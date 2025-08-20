import llm_utils as llm_utils
import os
import json

class UCDAgent:
    def __init__(self,input_text):
        self.input_text = input_text
        self.actors = []
        self.usecases = []
        self.association_relationships = {}
        self.inclusion_relationships = {}
        self.extension_relationships = {}
        self.generalization_relationships_for_usecases = {}
        self.generalization_relationships_for_actors = {}
        self.usecase_actor_dict = {}


    def extract_actors(self):
        print("========Extracting Actors========")
        # 读取参与者提取prompt模板和示例
        extract_actors_prompt = open("../prompts/ea_template.txt", encoding='utf-8').read()
        few_shot_examples_str = open("../few_shot_examples/ea_few_shot_examples.txt", encoding='utf-8').read()
        filled_prompt = extract_actors_prompt.format_map(
            {
                "few_shot_examples": few_shot_examples_str, 
                "input_text": self.input_text}
        )
        # 提取参与者
        messages = [{"role": "user", "content": filled_prompt}]
        completion = llm_utils.openai_chat_completion("You are an expert in the field of requirement modeling", messages)
        # messages.append({"role": "assistant", "content": completion})
        # # 参与者反思
        # revise_actors_prompt = open("../prompts/ear_template.txt", encoding='utf-8').read()
        # messages.append({'role': 'user', 'content': revise_actors_prompt})
        # completion = llm_utils.openai_chat_completion(None, messages)
        self.actors = llm_utils.parse_raw_list_answers(completion)

    def extract_usecases(self):
        print("========Extracting Use Cases========")
        # 读取用例提取prompt模板和示例
        extract_usecases_prompt = open("../prompts/eu_template.txt", encoding='utf-8').read()
        few_shot_examples_str = open("../few_shot_examples/eu_few_shot_examples.txt", encoding='utf-8').read()
        with open("../prompts/eur_template.txt", encoding='utf-8') as f:
            revise_usecases_prompt = f.read()
        for actor in self.actors:
            filled_prompt = extract_usecases_prompt.format_map(
                {
                    "few_shot_examples": few_shot_examples_str, 
                    "input_text": self.input_text,
                    "actor":actor}
            )
            # 提取参与者actor关联的用例
            messages = [{"role": "user", "content": filled_prompt}]
            completion = llm_utils.openai_chat_completion("You are an expert in the field of requirement modeling", messages)
            # messages.append({"role": "assistant", "content": completion})
            # # 用例反思
            # filled_prompt = revise_usecases_prompt.format_map(
            #     {
            #         "actor":actor}
            # )
            # messages.append({'role': 'user', 'content': filled_prompt})
            # completion = llm_utils.openai_chat_completion(None, messages)
            cur_usecases = llm_utils.parse_raw_list_answers(completion)
            self.association_relationships[actor] = cur_usecases
            self.usecases.extend(cur_usecases)
            # 将参与者与用例的关联存储在字典中
            for usecase in cur_usecases:
                if usecase not in self.usecase_actor_dict:
                    self.usecase_actor_dict[usecase] = []
                self.usecase_actor_dict[usecase].append(actor)
        # 去重
        self.usecases = list(set(self.usecases))

    def prejudge_usecase_associations(self,usecase1: str ,usecase2: str):
        print("========Prejudge Agent Starts Working========")
        # 读取初判智能体prompt模板
        with open("../prompts/pre_eua_template.txt", encoding='utf-8') as f:
            prejudge_ua_prompts = f.read()
        filled_prompt = prejudge_ua_prompts.format_map(
                { 
                    "input_text": self.input_text,
                    "usecase1":usecase1,
                    "usecase2":usecase2}
            )
        # 确定需要讨论的问题及双方观点
        messages = [{"role": "user", "content": filled_prompt}]
        # print(f"Prejudge Agent Prompt: {filled_prompt}\n")
        completion = llm_utils.openai_chat_completion("You are an expert in the field of requirement modeling", messages)
        answer_list = llm_utils.parse_raw_list_answers(completion)
        return answer_list

    def get_actors_of_usecase(self, usecase):
        actors = self.usecase_actor_dict.get(usecase, [])
        actors_str = '/'.join(actors) if actors else ''
        return usecase+' for '+actors_str

    def extract_usecase_associations(self):
        print("========Extracting Use Case Associations========")
        print(f"当前用例列表：{self.usecases}")
        for i in range(len(self.usecases)):
            for j in range(len(self.usecases)):
                if j>i:
                    final_option = ''
                    pre_answer_list = self.prejudge_usecase_associations(self.get_actors_of_usecase(self.usecases[i]),self.get_actors_of_usecase(self.usecases[j]))
                    if len(pre_answer_list) == 1:
                        final_option = pre_answer_list[0]
                    else:
                        print("========Debate Agents Start Working========")
                        # 第一轮：陈述观点
                        debater1_opinion = llm_utils.get_opinion(pre_answer_list[0],self.usecases[i],self.usecases[j])
                        print(f"智能体1的观点：{debater1_opinion}")
                        debater2_opinion = llm_utils.get_opinion(pre_answer_list[1],self.usecases[i],self.usecases[j])
                        print(f"智能体2的观点：{debater2_opinion}")
                        with open("../prompts/debate_template.txt", encoding='utf-8') as f:
                            debate_prompts = f.read()
                        # 智能体1陈述观点
                        debater1_prompt = debate_prompts.format_map(
                                {
                                    "input_text": self.input_text,
                                    "usecase1":self.get_actors_of_usecase(self.usecases[i]),
                                    "usecase2":self.get_actors_of_usecase(self.usecases[j]),
                                    "debater1_opinion":debater1_opinion,
                                    "debater2_opinion":debater2_opinion}
                        )
                        debater1_messages = [{"role": "user", "content": debater1_prompt}]
                        debater1_rsp = llm_utils.openai_chat_completion("You are an expert in the field of requirement modeling", debater1_messages)
                        debater1_messages.append({"role": "assistant", "content": debater1_rsp})
                        # 智能体2陈述观点
                        debater2_prompt = debate_prompts.format_map(
                                {
                                    "input_text": self.input_text,
                                    "usecase1":self.get_actors_of_usecase(self.usecases[i]),
                                    "usecase2":self.get_actors_of_usecase(self.usecases[j]),
                                    "debater1_opinion":debater2_opinion,
                                    "debater2_opinion":debater1_opinion}
                        )
                        debater2_messages = [{"role": "user", "content": debater2_prompt}]
                        debater2_rsp = llm_utils.openai_chat_completion("You are an expert in the field of requirement modeling", debater2_messages)
                        debater2_messages.append({"role": "assistant", "content": debater2_rsp})
                        # 第一轮结束，裁判智能体投票
                        print("========Judge Agent Starts Working========")
                        vote_counter = {'0' : 0, '1': 0, '2': 0}
                        with open("../prompts/judge_template.txt", encoding='utf-8') as f:
                            judge_prompt_template = f.read()
                        judge_prompt = judge_prompt_template.format_map(
                        {
                                "input_text": self.input_text,
                                "debater1_statement":debater1_rsp.strip(),
                                "debater2_statement":debater2_rsp.strip()}
                            )
                        judge_messages = [{"role": "user", "content": judge_prompt}]
                        judge_rsp = llm_utils.openai_chat_completion("You are an expert in the field of requirement modeling", judge_messages)
                        judge_messages.append({"role": "assistant", "content": judge_rsp})
                        if '0' in judge_rsp:
                            vote_counter['0'] += 1
                        elif '1' in judge_rsp:
                            vote_counter['1'] += 1
                        elif '2' in judge_rsp:
                            vote_counter['2'] += 1
                        # 第二轮：反驳对方观点
                        debater1_messages.append({"role": "user", "content": f'Previous round of opponent\'s speech: {debater2_rsp.strip()}\nNow you can start the second round of rebuttal.'})
                        debater2_messages.append({"role": "user", "content": f'Previous round of opponent\'s speech: {debater1_rsp.strip()}\nNow you can start the second round of rebuttal.'})
                        debater1_rsp = llm_utils.openai_chat_completion(None, debater1_messages)
                        debater1_messages.append({"role": "assistant", "content": debater1_rsp})
                        debater2_rsp = llm_utils.openai_chat_completion(None, debater2_messages)
                        debater2_messages.append({"role": "assistant", "content": debater2_rsp})
                        # 第二轮结束，裁判智能体投票
                        judge_messages.append({
                            "role": "user",
                            "content": (f'Debater 1\'s speech is as follows: {debater1_rsp.strip()}'
                                            f'Debater 2\'s speech is as follows: {debater2_rsp.strip()}')
                        })
                        judge_rsp = llm_utils.openai_chat_completion(None, judge_messages)
                        judge_messages.append({"role": "assistant", "content": judge_rsp})
                        if '0' in judge_rsp:
                            vote_counter['0'] += 1
                        elif '1' in judge_rsp:
                            vote_counter['1'] += 1
                        elif '2' in judge_rsp:
                            vote_counter['2'] += 1
                        # 第三轮：总结结论，确定最终观点
                        debater1_messages.append({"role": "user", "content": f'Previous round of opponent\'s speech: {debater2_rsp.strip()}\nNow you can start the third round of conclusion. Please output \'persist\' or \'abandon\''})
                        debater2_messages.append({"role": "user", "content": f'Previous round of opponent\'s speech: {debater1_rsp.strip()}\nNow you can start the third round of conclusion. Please output \'persist\' or \'abandon\''})
                        debater1_rsp = llm_utils.openai_chat_completion(None, debater1_messages)
                        debater1_messages.append({"role": "assistant", "content": debater1_rsp})
                        debater2_rsp = llm_utils.openai_chat_completion(None, debater2_messages)
                        debater2_messages.append({"role": "assistant", "content": debater2_rsp})
                        if 'persist' in debater1_rsp.lower():
                            vote_counter['1'] += 1
                        elif 'abandon' in debater1_rsp.lower():
                            vote_counter['2'] += 1
                        if 'abandon' in debater2_rsp.lower():
                            vote_counter['1'] += 1
                        elif 'persist' in debater2_rsp.lower():
                            vote_counter['2'] += 1
                        # 第三轮结束，裁判智能体投票
                        judge_messages.append({
                            "role": "user",
                            "content": (f'Debater 1\'s speech is as follows: I {debater1_rsp.strip()} my viewpoint.\n'
                                            f'Debater 2\'s speech is as follows: I {debater2_rsp.strip()} my viewpoint.\n')
                        })
                        judge_rsp = llm_utils.openai_chat_completion(None, judge_messages)
                        judge_messages.append({"role": "assistant", "content": judge_rsp})
                        if '0' in judge_rsp:
                            vote_counter['0'] += 1
                        elif '1' in judge_rsp:
                            vote_counter['1'] += 1
                        elif '2' in judge_rsp:
                            vote_counter['2'] += 1
                        # vote_counter[judge_rsp[0]] += 1

                        # print(f"辩论智能体1的对话历史：{debater1_messages}")
                        # print(f"辩论智能体2的对话历史：{debater2_messages}")
                        # print(f"裁判智能体的对话历史：{judge_messages}")
                        # 统计投票结果，确定最终观点
                        max_vote = max(vote_counter, key=vote_counter.get)
                        if vote_counter['0'] > 0 :
                            final_option = 'G'
                        else:
                            final_option = pre_answer_list[int(max_vote) - 1]
                        print(vote_counter)
                    print(final_option)
                    if final_option == 'A':
                        self.inclusion_relationships.setdefault(self.usecases[i], []).append(self.usecases[j])
                    elif final_option == 'B':
                        self.inclusion_relationships.setdefault(self.usecases[j], []).append(self.usecases[i])
                    elif final_option == 'C':
                        self.extension_relationships.setdefault(self.usecases[j], []).append(self.usecases[i])
                    elif final_option == 'D':
                        self.extension_relationships.setdefault(self.usecases[i], []).append(self.usecases[j])
                    elif final_option == 'E':
                        self.generalization_relationships_for_usecases.setdefault(self.usecases[j], []).append(self.usecases[i])
                    elif final_option == 'F':
                        self.generalization_relationships_for_usecases.setdefault(self.usecases[i], []).append(self.usecases[j])

    def extract_actor_relationships(self):
        print("========Extracting Actor Relationships========")
        # 读取参与者泛化关系提取prompt模板
        extract_generalization_prompt = open("../prompts/egra_template.txt", encoding='utf-8').read()
        for i in range(len(self.actors)):
            for j in range(len(self.actors)):
                if j > i:
                    filled_prompt = extract_generalization_prompt.format_map(
                        {
                            "input_text": self.input_text,
                            "actor1": self.actors[i],
                            "actor2": self.actors[j]
                        }
                    )
                    messages = [{"role": "user", "content": filled_prompt}]
                    completion = llm_utils.openai_chat_completion("You are an expert in the field of requirement modeling", messages)
                    final_output = llm_utils.parse_raw_tuple(completion)
                    if final_output:
                        if final_output[0] not in self.generalization_relationships_for_actors:
                            self.generalization_relationships_for_actors[final_output[0]] = []
                        self.generalization_relationships_for_actors[final_output[0]].append(final_output[1])
                    else:
                        print(f"No generalization relationship between {self.actors[i]} and {self.actors[j]}")

    # 删除关联关系列表中多余子用例(功能小函数)
    def delete_usecases(self):
        usecases_to_cut = set()
        for key, list_value in self.inclusion_relationships.items():
            usecases_to_cut.update(list_value)
        for key, list_value in self.extension_relationships.items():
            usecases_to_cut.update(list_value)
        for key, list_value in self.generalization_relationships_for_usecases.items():
            usecases_to_cut.update(list_value)
        usecases_to_cut = list(usecases_to_cut)
        print(f'删除多余子用例：{usecases_to_cut}')
        # 遍历关联关系列表删除多余的子用例
        for key, list_value in self.association_relationships.items():
            for item in usecases_to_cut:
                if item in list_value:
                    list_value.remove(item)

    # 删除关联关系列表中父参与者关联的多余用例（功能小函数）
    def delete_actor_usecases(self):
        for parent_actor, child_actors in self.generalization_relationships_for_actors.items():
            for child in child_actors:
                for usecase in self.association_relationships.get(parent_actor, []):
                    if usecase in self.association_relationships[child]:
                        self.association_relationships[child].remove(usecase)

    # 生成PlantUML格式用例图（功能小函数）
    def generate_diagram(self, plantuml_file:str):
        fp = open(plantuml_file, "w", encoding='utf-8')  
        # 开始
        print("@startuml\nleft to right direction", file=fp)
        # 参与者
        for actor in self.actors:
            print(f"actor \"{actor}\"", file=fp)
        # 用例
        for usecase in self.usecases:
            print(f"usecase \"{usecase}\"", file=fp)
        # 关联关系
        for key, list_value in self.association_relationships.items():
            for item in list_value:
                print(f"\"{key}\"--\"{item}\"", file=fp)
        # 包含关系
        for key, list_value in self.inclusion_relationships.items():
            for item in list_value:
                print(f"\"{item}\"<|.\"{key}\": <<include>>", file=fp)
        # 扩展关系
        for key, list_value in self.extension_relationships.items():
            for item in list_value:
                print(f"\"{key}\"<|.\"{item}\": <<extend>>", file=fp)
        # 泛化关系（用例间）
        for key, list_value in self.generalization_relationships_for_usecases.items():
            for item in list_value:
                print(f"\"{item}\"--|>\"{key}\"", file=fp)
        # 泛化关系（参与者间）
        for key, list_value in self.generalization_relationships_for_actors.items():
            for item in list_value:
                print(f"\"{item}\"--|>\"{key}\"", file=fp)
        # 结束
        print("@enduml", file=fp)
        fp.close()

    def save_to_json(self, json_file: str):
        data = {
            "actors": self.actors,
            "usecases": self.usecases,
            "association_relationships": self.association_relationships,
            "inclusion_relationships": self.inclusion_relationships,
            "extension_relationships": self.extension_relationships,
            "generalization_relationships_for_usecases": self.generalization_relationships_for_usecases,
            "generalization_relationships_for_actors": self.generalization_relationships_for_actors
        }
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)



# with open("../datasets/test.txt", "r") as file:
#     input_text = file.read().strip()
# UCD = UCDAgent(input_text)
# UCD.extract_actors()
# UCD.extract_usecases()
# UCD.extract_usecase_associations()
# UCD.extract_actor_relationships()
# UCD.save_to_json("../output/result.json")
# UCD.delete_usecases()
# UCD.delete_actor_usecases()
# UCD.generate_diagram("../output/result.txt")
# print("JSON file saved successfully.")