import numpy as np
import json
from collections import defaultdict
import requests
import time
from openai import OpenAI, RateLimitError, APIConnectionError, APIError
from config import BASE_URL, EMBEDDING_URL, OPENAI_API_KEY, OPENAI_MODEL, OPENAI_EMBEDDING_MODEL

entity_similarity_prompt = """
Given two actors (e.g. "User", "Administrator") or two use cases (e.g. "Log In", "Process Order"), you need to determine whether they refer to the same entity or concept based on the following rules. 
(1) If two items have the same or highly similar meaning (even if the wording is different), they are considered the same. Including synonyms, synonyms, and common variants;
Example: "Log In" and "Sign In" refer to the same operation; The roles of 'Manager' and 'Employee' are different.
(2) The singular and plural forms are assumed to refer to the same entity by default;
Example: "User" and "Users" are the same.
(3) Abbreviations and full names are considered the same, ignoring differences in capitalization, spaces, and hyphens. Minor spelling variations (such as American/British spelling) are considered the same;
Example: "Admin" and "Administrator" are the same.
(4) For actors (noun phrases), focus on determining whether the roles or entities are the same; For use cases (gerund phrases), focus on determining whether the operations are the same.
Example: "Create Account" and "Add Account" are the same; But 'Add account' and 'Remove account' are different.

Given the following two actors or use cases, apply the above rules to determine if they refer to the same.
Entity 1: {entity1}
Entity 2: {entity2}

Respond ONLY with a JSON object: {{"result": true}} if they are the same entity, or {{"result": false}} otherwise. Do not include any explanations.
"""

relation_similarity_prompt = """
Please evaluate the semantic similarity between two sets of relationships for the same actor/use case from different use case diagrams. Score between 0-1 where 1 means identical meaning and coverage.

Relationship Set A:
{relations1}

Relationship Set B:
{relations2}

Consider:
1. Completeness of information
2. Semantic equivalence of relationships
3. Consistency of connected actors/ use cases
4. Overall knowledge structure similarity

Return ONLY a JSON object with one key "similarity" representing the similarity score. Example: {{"similarity": 0.85}}
"""


def openai_chat_completion(model: str, system_prompt: str, history: list, temperature=0, max_tokens=512, max_retries=3,
                           retry_delay=1):
    client = OpenAI(
        api_key = OPENAI_API_KEY,
        base_url = BASE_URL
    )

    response = None
    if system_prompt is not None:
        messages = [{"role": "system", "content": system_prompt}] + history
    else:
        messages = history

    retry_count = 0
    while retry_count < max_retries:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            # print(f"LLM输出: {response.choices[0].message.content}")
            return response.choices[0].message.content
        except APIConnectionError as e:
            retry_count += 1
            print(f"连接错误: {e}. 正在重试 {retry_count}/{max_retries}...")
            if retry_count < max_retries:
                time.sleep(retry_delay)
        except RateLimitError as e:
            retry_count += 1
            print(f"速率限制错误: {e}. 正在重试 {retry_count}/{max_retries}...")
            if retry_count < max_retries:
                time.sleep(retry_delay * 2)  # 速率限制错误时增加延迟
        except APIError as e:
            retry_count += 1
            print(f"API错误: {e}. 正在重试 {retry_count}/{max_retries}...")
            if retry_count < max_retries:
                time.sleep(retry_delay)
        except Exception as e:
            print(f"未知错误: {e}")
            break

    # 如果所有重试都失败，返回错误信息
    return f"请求失败，已达到最大重试次数 {max_retries}"


class KGEvaluator:
    def __init__(self, kg_standard, kg_eval):
        self.kg_standard = kg_standard
        self.kg_eval = kg_eval

        # Preprocess KG structures
        self.std_entities, self.std_relations = self.preprocess_kg(kg_standard)
        self.eval_entities, self.eval_relations = self.preprocess_kg(kg_eval)

    def preprocess_kg(self, json_data):
        # 初始化实体和关系字典
        entities = {}
        relations = defaultdict(list)

        # 添加参与者实体
        for actor in json_data['actors']:
            entities[actor] = {'name': actor, 'type': 'actor'}

        # 添加用例实体
        for usecase in json_data['usecases']:
            entities[usecase] = {'name': usecase, 'type': 'usecase'}

        # 添加关联关系
        for actor, usecases in json_data['association_relationships'].items():
            for usecase in usecases:
                relations[actor].append([actor, 'ASSOCIATED_WITH', usecase])

        # 添加包含关系
        for usecase, included_usecases in json_data['inclusion_relationships'].items():
            for included_usecase in included_usecases:
                relations[usecase].append([usecase, 'INCLUDES', included_usecase])

        # 添加扩展关系
        for usecase, extended_usecases in json_data['extension_relationships'].items():
            for extended_usecase in extended_usecases:
                relations[usecase].append([usecase, 'EXTENDS', extended_usecase])

        # 添加用例间泛化关系
        for general_usecase, specific_usecases in json_data['generalization_relationships_for_usecases'].items():
            for specific_usecase in specific_usecases:
                relations[general_usecase].append([general_usecase, 'USECASE_GENERALIZES', specific_usecase])

        # 添加参与者泛化关系
        for general_actor, specific_actors in json_data['generalization_relationships_for_actors'].items():
            for specific_actor in specific_actors:
                relations[general_actor].append([general_actor, 'ACTOR_GENERALIZES', specific_actor])

        return entities, relations

    def _get_embedding(self, text):
        """Get text embedding vector"""
        url = EMBEDDING_URL
        payload = {
            "model": OPENAI_EMBEDDING_MODEL,
            "input": text,
            "encoding_format": "float"
        }
        headers = {
            "Authorization": "Bearer sk-kaxxsbjadwlsgsspwodimxdtngrwnsxekzurieucfboilhok",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        data = json.loads(response.text)
        # 提取 embedding 列表
        embedding_list = data['data'][0]['embedding']
        # 输出 embedding 列表
        return embedding_list

    def _find_candidate_matches(self, threshold=0.8):
        """Find all candidate matching entity pairs"""
        # Generate standard entity text
        std_texts = {
            name: f"{e['name'].lower()} {e.get('type', '')}"
            for name, e in self.std_entities.items()
        }
        # Generate evaluation entity text
        eval_texts = {
            name: f"{e['name'].lower()} {e.get('type', '')}"
            for name, e in self.eval_entities.items()
        }

        # Calculate embedding vectors
        std_embeddings = {k: self._get_embedding(v) for k, v in std_texts.items()}
        eval_embeddings = {k: self._get_embedding(v) for k, v in eval_texts.items()}

        # Calculate similarity matrix
        candidates = []
        for s_name, s_vec in std_embeddings.items():
            for e_name, e_vec in eval_embeddings.items():
                if self.std_entities[s_name]['type']!= self.eval_entities[e_name]['type']:
                    continue
                sim = np.array([s_vec]) @ np.array(e_vec).T
                sim = sim[0]
                if sim > threshold:
                    candidates.append((s_name, e_name, sim))
                    print(f"Found candidate match: {s_name} <-> {e_name} with similarity {sim:.4f}")

        # Sort by similarity
        return sorted(candidates, key=lambda x: -x[2])

    def _llm_judge_entity(self, entity1, entity2):
        """Use LLM to judge if entities are the same"""
        filled_prompt = entity_similarity_prompt.format_map(
            {
                "entity1": json.dumps(entity1, ensure_ascii=False),
                "entity2": json.dumps(entity2, ensure_ascii=False)
            }
        )
        print(f"{entity1['name']} vs {entity2['name']}")
        messages = [{"role": "user", "content": filled_prompt}]
        # print(f"Prompt: {filled_prompt}")
        completion = openai_chat_completion(OPENAI_MODEL, "You are an expert in entity disambiguation.", messages)
        print(f"LLM输出: {completion}")
        try:
            return json.loads(completion)['result']
        except:
            return False

    def _llm_relation_similarity(self, rels1, rels2):
        """Use LLM to evaluate relation similarity"""

        def format_rels(rels):
            formatted = []
            for rel in rels:
                head, r, tail= rel[:3]
                formatted.append(f"{head} --{r}-> {tail}".strip())
            return "\n".join(formatted) or "No relationships"

        filled_prompt = relation_similarity_prompt.format_map(
            {
                "relations1": format_rels(rels1),
                "relations2": format_rels(rels2)
            }
        )
        print(f"{rels1} vs {rels2}")
        messages = [{"role": "user", "content": filled_prompt}]
        # print(f"Prompt: {filled_prompt}")
        completion = openai_chat_completion(OPENAI_MODEL, "You are an expert in relation disambiguation. ", messages)
        print(f"LLM输出: {completion}")
        try:
            return json.loads(completion)['similarity']
        except:
            return 0.0

    def evaluate(self):
        """Execute evaluation process"""
        # Step 1: Find all candidate matches
        candidates = self._find_candidate_matches()
        print(candidates)

        # Step 2: LLM confirms matches
        matched_pairs = []
        matched_eval_entities = set()

        for s_name, e_name, sim in candidates:
            if s_name in matched_eval_entities:
                continue  # Each standard entity is matched only once
            std_entity = self.std_entities[s_name]
            eval_entity = self.eval_entities[e_name]
            if abs(sim - 1.0) < 1e-4:   # 完全一样则无需大模型判断
                matched_pairs.append((std_entity, eval_entity))
                matched_eval_entities.add(s_name)
                print(f"Confirmed match: {std_entity['name']} <-> {eval_entity['name']}")
                continue
            if self._llm_judge_entity(std_entity, eval_entity):
                matched_pairs.append((std_entity, eval_entity))
                matched_eval_entities.add(s_name)
                print(f"Confirmed match: {std_entity['name']} <-> {eval_entity['name']}")

        # Calculate metrics
        entity_cover = len(matched_pairs)
        print(entity_cover)
        total_std_entities = len(self.std_entities)
        total_eval_entities = len(self.eval_entities)
        print(total_std_entities)
        print(total_eval_entities)
        entity_recall = entity_cover / total_std_entities if total_std_entities else 0.0
        entity_precision = entity_cover / total_eval_entities if total_eval_entities else 0.0
        entity_F1 = 2 * entity_recall * entity_precision / (entity_recall + entity_precision)

        # 创建待评估实体到标准实体的映射字典
        eval_to_std = {eval_ent['name']: std_ent['name'] for std_ent, eval_ent in matched_pairs}
        # 获取匹配的标准实体集合
        matched_std_entities = set(std_ent['name'] for std_ent, _ in matched_pairs)
        # 构建标准三元组集合（只包含完全匹配的三元组）
        valid_std_triples = set()

        merged_std_list = [item for sublist in self.std_relations.values() for item in sublist]
        for h, r, t in merged_std_list:
            # 只保留头尾实体都匹配的三元组
            if h in matched_std_entities and t in matched_std_entities:
                valid_std_triples.add((h, r, t))
        # 构建转换后的待评估三元组集合
        converted_eval_triples = set()
        merged_eval_list = [item for sublist in self.eval_relations.values() for item in sublist]
        for h, r, t in merged_eval_list:
            # 检查头尾实体是否都能映射到标准实体
            if h in eval_to_std and t in eval_to_std:
                std_h = eval_to_std[h]
                std_t = eval_to_std[t]
                converted_eval_triples.add((std_h, r, std_t))

        # 计算关系三元组指标
        tp = len(valid_std_triples & converted_eval_triples)  # 真正例
        total_eval_relations = len(merged_eval_list)
        total_std_relations = len(merged_std_list)
        # 计算精确率、召回率和F1
        relation_precision = tp / total_eval_relations if total_eval_relations > 0 else 0.0
        relation_recall = tp / total_std_relations if total_std_relations > 0 else 0.0
        relation_F1 = (2 * relation_precision * relation_recall /
                       (relation_precision + relation_recall)) if relation_precision + relation_recall > 0 else 0.0

        # rel_similarities = []
        # total_weight = 0
        # for std_ent, eval_ent in matched_pairs:
        #     std_rels = self.std_relations.get(std_ent['name'], [])
        #     eval_rels = self.eval_relations.get(eval_ent['name'], [])
        #     if std_rels == [] and eval_rels == []:
        #         continue
        #     weight = np.log(len(std_rels) + 1)  # 避免零度
        #     total_weight += weight
        #     sim = self._llm_relation_similarity(std_rels, eval_rels)
        #     print(f"final_sim: {sim}")
        #     rel_similarities.append(sim * weight)
        #
        # # avg_rel_sim = sum(rel_similarities) / len(rel_similarities) if rel_similarities else 0.0
        # avg_rel_sim = sum(rel_similarities) / total_weight if rel_similarities else 0.0

        return {
            "entity_recall": round(entity_recall, 4),
            "entity_precision": round(entity_precision,4),
            "entity_F1":round(entity_F1,4),
            # "relation_similarity": round(avg_rel_sim, 4),
            "relation_recall": round(relation_recall, 4),
            "relation_precision": round(relation_precision, 4),
            "relation_F1": round(relation_F1, 4),
        }


if __name__ == "__main__":
    # Specify output file path
    output_file = "ablation_eval_results.jsonl"

    with open(output_file, "a", encoding="utf-8") as out_f:
        for i in range(1,61):
            lower = ((i - 1) // 10) * 10 + 1
            upper = lower + 9
            # Read clean data
            clean_file = f"../../datasets/60_ideal_UCD/{lower}-{upper}/{i}_result.json"
            with open(clean_file, "r") as f1:
                data_clean = json.load(f1)
            print("Successfully imported ideal data")

            # Read Qwen_wo_DM data
            Qwen_wo_DM_file = f"../../ablation_output/Qwen_wo_DM/{i}_result.json"
            with open(Qwen_wo_DM_file, "r") as f2:
                data_Qwen_wo_DM = json.load(f2)
            print("Successfully imported Qwen_wo_DM data")

            # Read Qwen_wo_SR data
            Qwen_wo_SR_file = f"../../ablation_output/Qwen_wo_SR/{i}_result.json"
            with open(Qwen_wo_SR_file, "r") as f3:
                data_Qwen_wo_SR = json.load(f3)
            print("Successfully imported Qwen_wo_SR data")

            print("Using standard kg as reference")

            evaluator = KGEvaluator(data_clean, data_Qwen_wo_DM)
            results_Qwen_wo_DM = evaluator.evaluate()
            print("Evaluating Qwen_wo_DM")
            print(f"Entity Recall: {results_Qwen_wo_DM['entity_recall']}")
            print(f"Entity Precision: {results_Qwen_wo_DM['entity_precision']}")
            print(f"Entity F1: {results_Qwen_wo_DM['entity_F1']}")
            print(f"Relation Recall: {results_Qwen_wo_DM['relation_recall']}")
            print(f"Relation Precision: {results_Qwen_wo_DM['relation_precision']}")
            print(f"Relation F1: {results_Qwen_wo_DM['relation_F1']}")

            evaluator = KGEvaluator(data_clean, data_Qwen_wo_SR)
            results_Qwen_wo_SR = evaluator.evaluate()
            print("Evaluating Qwen_wo_SR")
            print(f"Entity Recall: {results_Qwen_wo_SR['entity_recall']}")
            print(f"Entity Precision: {results_Qwen_wo_SR['entity_precision']}")
            print(f"Entity F1: {results_Qwen_wo_SR['entity_F1']}")
            print(f"Relation Recall: {results_Qwen_wo_SR['relation_recall']}")
            print(f"Relation Precision: {results_Qwen_wo_SR['relation_precision']}")
            print(f"Relation F1: {results_Qwen_wo_SR['relation_F1']}")


            # Construct result dictionary according to example requirements (adjust key names as needed)
            out_data = {
                "data_id": i,
                "Qwen_wo_DM": {
                    "Entity Recall": results_Qwen_wo_DM["entity_recall"],
                    "Entity Precision": results_Qwen_wo_DM["entity_precision"],
                    "Entity F1": results_Qwen_wo_DM["entity_F1"],
                    "Relation Recall": results_Qwen_wo_DM["relation_recall"],
                    "Relation Precision": results_Qwen_wo_DM["relation_precision"],
                    "Relation F1": results_Qwen_wo_DM["relation_F1"],
                },
                "Qwen_wo_SR":{
                    "Entity Recall": results_Qwen_wo_SR["entity_recall"],
                    "Entity Precision": results_Qwen_wo_SR["entity_precision"],
                    "Entity F1": results_Qwen_wo_SR["entity_F1"],
                    "Relation Recall": results_Qwen_wo_SR["relation_recall"],
                    "Relation Precision": results_Qwen_wo_SR["relation_precision"],
                    "Relation F1": results_Qwen_wo_SR["relation_F1"],
                },
            }

            # Write results to JSONL file, one JSON object per line
            out_f.write(json.dumps(out_data, ensure_ascii=False) + "\n")


