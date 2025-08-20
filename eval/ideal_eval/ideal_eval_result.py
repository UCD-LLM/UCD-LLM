import json
import statistics

# 初始化存储各指标值的列表
Qwen_UCD_entity_recall = []
Qwen_UCD_entity_precision = []
Qwen_UCD_entity_F1 = []
Qwen_UCD_relation_recall = []
Qwen_UCD_relation_precision = []
Qwen_UCD_relation_F1 = []
# Qwen_UCD_relation_similarity = []

Qwen_single_entity_recall = []
Qwen_single_entity_precision = []
Qwen_single_entity_F1 = []
Qwen_single_relation_recall = []
Qwen_single_relation_precision = []
Qwen_single_relation_F1 = []
# Qwen_single_relation_similarity = []

DeepSeek_UCD_entity_recall = []
DeepSeek_UCD_entity_precision = []
DeepSeek_UCD_entity_F1 = []
DeepSeek_UCD_relation_recall = []
DeepSeek_UCD_relation_precision = []
DeepSeek_UCD_relation_F1 = []
# DeepSeek_UCD_relation_similarity = []

DeepSeek_single_entity_recall = []
DeepSeek_single_entity_precision = []
DeepSeek_single_entity_F1 = []
DeepSeek_single_relation_recall = []
DeepSeek_single_relation_precision = []
DeepSeek_single_relation_F1 = []
# DeepSeek_single_relation_similarity = []

GLM_UCD_entity_recall = []
GLM_UCD_entity_precision = []
GLM_UCD_entity_F1 = []
GLM_UCD_relation_recall = []
GLM_UCD_relation_precision = []
GLM_UCD_relation_F1 = []
# GLM_UCD_relation_similarity = []

GLM_single_entity_recall = []
GLM_single_entity_precision = []
GLM_single_entity_F1 = []
GLM_single_relation_recall = []
GLM_single_relation_precision = []
GLM_single_relation_F1 = []
# GLM_single_relation_similarity = []

# IT4RE_entity_recall = []
# IT4RE_entity_precision = []
# IT4RE_entity_F1 = []
# IT4RE_relation_similarity = []


# 读取 JSONL 文件
file_path = 'ideal_eval_results.jsonl'
with open(file_path, 'r') as file:
    for line in file:
        # 解析每行的 JSON 数据
        data = json.loads(line)

        # 提取三个字段的数据
        Qwen_UCD = data['Qwen_UCD']
        Qwen_single = data['Qwen_single']
        DeepSeek_UCD = data['DeepSeek_UCD']
        DeepSeek_single = data['DeepSeek_single']
        GLM_UCD = data['GLM_UCD']
        GLM_single = data['GLM_single']
        # IT4RE = data['IT4RE']

        # 将指标值添加到对应的列表中
        Qwen_UCD_entity_recall.append(Qwen_UCD['Entity Recall'])
        Qwen_UCD_entity_precision.append(Qwen_UCD['Entity Precision'])
        Qwen_UCD_entity_F1.append(Qwen_UCD['Entity F1'])
        Qwen_UCD_relation_recall.append(Qwen_UCD['Relation Recall'])
        Qwen_UCD_relation_precision.append(Qwen_UCD['Relation Precision'])
        Qwen_UCD_relation_F1.append(Qwen_UCD['Relation F1'])
        # Qwen_UCD_relation_similarity.append(Qwen_UCD['Relation Similarity'])

        Qwen_single_entity_recall.append(Qwen_single['Entity Recall'])
        Qwen_single_entity_precision.append(Qwen_single['Entity Precision'])
        Qwen_single_entity_F1.append(Qwen_single['Entity F1'])
        Qwen_single_relation_recall.append(Qwen_single['Relation Recall'])
        Qwen_single_relation_precision.append(Qwen_single['Relation Precision'])
        Qwen_single_relation_F1.append(Qwen_single['Relation F1'])
        # Qwen_single_relation_similarity.append(Qwen_single['Relation Similarity'])

        DeepSeek_UCD_entity_recall.append(DeepSeek_UCD['Entity Recall'])
        DeepSeek_UCD_entity_precision.append(DeepSeek_UCD['Entity Precision'])
        DeepSeek_UCD_entity_F1.append(DeepSeek_UCD['Entity F1'])
        DeepSeek_UCD_relation_recall.append(DeepSeek_UCD['Relation Recall'])
        DeepSeek_UCD_relation_precision.append(DeepSeek_UCD['Relation Precision'])
        DeepSeek_UCD_relation_F1.append(DeepSeek_UCD['Relation F1'])
        # DeepSeek_UCD_relation_similarity.append(DeepSeek_UCD['Relation Similarity'])

        DeepSeek_single_entity_recall.append(DeepSeek_single['Entity Recall'])
        DeepSeek_single_entity_precision.append(DeepSeek_single['Entity Precision'])
        DeepSeek_single_entity_F1.append(DeepSeek_single['Entity F1'])
        DeepSeek_single_relation_recall.append(DeepSeek_single['Relation Recall'])
        DeepSeek_single_relation_precision.append(DeepSeek_single['Relation Precision'])
        DeepSeek_single_relation_F1.append(DeepSeek_single['Relation F1'])
        # DeepSeek_single_relation_similarity.append(DeepSeek_single['Relation Similarity'])

        GLM_UCD_entity_recall.append(GLM_UCD['Entity Recall'])
        GLM_UCD_entity_precision.append(GLM_UCD['Entity Precision'])
        GLM_UCD_entity_F1.append(GLM_UCD['Entity F1'])
        GLM_UCD_relation_recall.append(GLM_UCD['Relation Recall'])
        GLM_UCD_relation_precision.append(GLM_UCD['Relation Precision'])
        GLM_UCD_relation_F1.append(GLM_UCD['Relation F1'])
        # GLM_UCD_relation_similarity.append(GLM_UCD['Relation Similarity'])

        GLM_single_entity_recall.append(GLM_single['Entity Recall'])
        GLM_single_entity_precision.append(GLM_single['Entity Precision'])
        GLM_single_entity_F1.append(GLM_single['Entity F1'])
        GLM_single_relation_recall.append(GLM_single['Relation Recall'])
        GLM_single_relation_precision.append(GLM_single['Relation Precision'])
        GLM_single_relation_F1.append(GLM_single['Relation F1'])
        # GLM_single_relation_similarity.append(GLM_single['Relation Similarity'])

        # IT4RE_entity_recall.append(IT4RE['Entity Recall'])
        # IT4RE_entity_precision.append(IT4RE['Entity Precision'])
        # IT4RE_entity_F1.append(IT4RE['Entity F1'])
        # IT4RE_relation_similarity.append(IT4RE['Relation Similarity'])


# 计算均值和方差
Qwen_UCD_er_mean = statistics.mean(Qwen_UCD_entity_recall)
Qwen_UCD_er_var = statistics.variance(Qwen_UCD_entity_recall)
Qwen_UCD_ep_mean = statistics.mean(Qwen_UCD_entity_precision)
Qwen_UCD_ep_var = statistics.variance(Qwen_UCD_entity_precision)
Qwen_UCD_ef_mean = statistics.mean(Qwen_UCD_entity_F1)
Qwen_UCD_ef_var = statistics.variance(Qwen_UCD_entity_F1)
Qwen_UCD_rr_mean = statistics.mean(Qwen_UCD_relation_recall)
Qwen_UCD_rr_var = statistics.variance(Qwen_UCD_relation_recall)
Qwen_UCD_rp_mean = statistics.mean(Qwen_UCD_relation_precision)
Qwen_UCD_rp_var = statistics.variance(Qwen_UCD_relation_precision)
Qwen_UCD_rf_mean = statistics.mean(Qwen_UCD_relation_F1)
Qwen_UCD_rf_var = statistics.variance(Qwen_UCD_relation_F1)
# Qwen_UCD_rs_mean = statistics.mean(Qwen_UCD_relation_similarity)
# Qwen_UCD_rs_var = statistics.variance(Qwen_UCD_relation_similarity)

Qwen_single_er_mean = statistics.mean(Qwen_single_entity_recall)
Qwen_single_er_var = statistics.variance(Qwen_single_entity_recall)
Qwen_single_ep_mean = statistics.mean(Qwen_single_entity_precision)
Qwen_single_ep_var = statistics.variance(Qwen_single_entity_precision)
Qwen_single_ef_mean = statistics.mean(Qwen_single_entity_F1)
Qwen_single_ef_var = statistics.variance(Qwen_single_entity_F1)
Qwen_single_rr_mean = statistics.mean(Qwen_single_relation_recall)
Qwen_single_rr_var = statistics.variance(Qwen_single_relation_recall)
Qwen_single_rp_mean = statistics.mean(Qwen_single_relation_precision)
Qwen_single_rp_var = statistics.variance(Qwen_single_relation_precision)
Qwen_single_rf_mean = statistics.mean(Qwen_single_relation_F1)
Qwen_single_rf_var = statistics.variance(Qwen_single_relation_F1)
# Qwen_single_rs_mean = statistics.mean(Qwen_single_relation_similarity)
# Qwen_single_rs_var = statistics.variance(Qwen_single_relation_similarity)

DeepSeek_UCD_er_mean = statistics.mean(DeepSeek_UCD_entity_recall)
DeepSeek_UCD_er_var = statistics.variance(DeepSeek_UCD_entity_recall)
DeepSeek_UCD_ep_mean = statistics.mean(DeepSeek_UCD_entity_precision)
DeepSeek_UCD_ep_var = statistics.variance(DeepSeek_UCD_entity_precision)
DeepSeek_UCD_ef_mean = statistics.mean(DeepSeek_UCD_entity_F1)
DeepSeek_UCD_ef_var = statistics.variance(DeepSeek_UCD_entity_F1)
DeepSeek_UCD_rr_mean = statistics.mean(DeepSeek_UCD_relation_recall)
DeepSeek_UCD_rr_var = statistics.variance(DeepSeek_UCD_relation_recall)
DeepSeek_UCD_rp_mean = statistics.mean(DeepSeek_UCD_relation_precision)
DeepSeek_UCD_rp_var = statistics.variance(DeepSeek_UCD_relation_precision)
DeepSeek_UCD_rf_mean = statistics.mean(DeepSeek_UCD_relation_F1)
DeepSeek_UCD_rf_var = statistics.variance(DeepSeek_UCD_relation_F1)
# DeepSeek_UCD_rs_mean = statistics.mean(DeepSeek_UCD_relation_similarity)
# DeepSeek_UCD_rs_var = statistics.variance(DeepSeek_UCD_relation_similarity)

DeepSeek_single_er_mean = statistics.mean(DeepSeek_single_entity_recall)
DeepSeek_single_er_var = statistics.variance(DeepSeek_single_entity_recall)
DeepSeek_single_ep_mean = statistics.mean(DeepSeek_single_entity_precision)
DeepSeek_single_ep_var = statistics.variance(DeepSeek_single_entity_precision)
DeepSeek_single_ef_mean = statistics.mean(DeepSeek_single_entity_F1)
DeepSeek_single_ef_var = statistics.variance(DeepSeek_single_entity_F1)
DeepSeek_single_rr_mean = statistics.mean(DeepSeek_single_relation_recall)
DeepSeek_single_rr_var = statistics.variance(DeepSeek_single_relation_recall)
DeepSeek_single_rp_mean = statistics.mean(DeepSeek_single_relation_precision)
DeepSeek_single_rp_var = statistics.variance(DeepSeek_single_relation_precision)
DeepSeek_single_rf_mean = statistics.mean(DeepSeek_single_relation_F1)
DeepSeek_single_rf_var = statistics.variance(DeepSeek_single_relation_F1)
# DeepSeek_single_rs_mean = statistics.mean(DeepSeek_single_relation_similarity)
# DeepSeek_single_rs_var = statistics.variance(DeepSeek_single_relation_similarity)

GLM_UCD_er_mean = statistics.mean(GLM_UCD_entity_recall)
GLM_UCD_er_var = statistics.variance(GLM_UCD_entity_recall)
GLM_UCD_ep_mean = statistics.mean(GLM_UCD_entity_precision)
GLM_UCD_ep_var = statistics.variance(GLM_UCD_entity_precision)
GLM_UCD_ef_mean = statistics.mean(GLM_UCD_entity_F1)
GLM_UCD_ef_var = statistics.variance(GLM_UCD_entity_F1)
GLM_UCD_rr_mean = statistics.mean(GLM_UCD_relation_recall)
GLM_UCD_rr_var = statistics.variance(GLM_UCD_relation_recall)
GLM_UCD_rp_mean = statistics.mean(GLM_UCD_relation_precision)
GLM_UCD_rp_var = statistics.variance(GLM_UCD_relation_precision)
GLM_UCD_rf_mean = statistics.mean(GLM_UCD_relation_F1)
GLM_UCD_rf_var = statistics.variance(GLM_UCD_relation_F1)
# GLM_UCD_rs_mean = statistics.mean(GLM_UCD_relation_similarity)
# GLM_UCD_rs_var = statistics.variance(GLM_UCD_relation_similarity)

GLM_single_er_mean = statistics.mean(GLM_single_entity_recall)
GLM_single_er_var = statistics.variance(GLM_single_entity_recall)
GLM_single_ep_mean = statistics.mean(GLM_single_entity_precision)
GLM_single_ep_var = statistics.variance(GLM_single_entity_precision)
GLM_single_ef_mean = statistics.mean(GLM_single_entity_F1)
GLM_single_ef_var = statistics.variance(GLM_single_entity_F1)
GLM_single_rr_mean = statistics.mean(GLM_single_relation_recall)
GLM_single_rr_var = statistics.variance(GLM_single_relation_recall)
GLM_single_rp_mean = statistics.mean(GLM_single_relation_precision)
GLM_single_rp_var = statistics.variance(GLM_single_relation_precision)
GLM_single_rf_mean = statistics.mean(GLM_single_relation_F1)
GLM_single_rf_var = statistics.variance(GLM_single_relation_F1)
# GLM_single_rs_mean = statistics.mean(GLM_single_relation_similarity)
# GLM_single_rs_var = statistics.variance(GLM_single_relation_similarity)

# IT4RE_er_mean = statistics.mean(IT4RE_entity_recall)
# IT4RE_er_var = statistics.variance(IT4RE_entity_recall)
# IT4RE_ep_mean = statistics.mean(IT4RE_entity_precision)
# IT4RE_ep_var = statistics.variance(IT4RE_entity_precision)
# IT4RE_ef_mean = statistics.mean(IT4RE_entity_F1)
# IT4RE_ef_var = statistics.variance(IT4RE_entity_F1)
# IT4RE_rs_mean = statistics.mean(IT4RE_relation_similarity)
# IT4RE_rs_var = statistics.variance(IT4RE_relation_similarity)



# 打印结果
print("Qwen_UCD Entity Recall: mean =", Qwen_UCD_er_mean, ", variance =", Qwen_UCD_er_var)
print("Qwen_UCD Entity Precision: mean =", Qwen_UCD_ep_mean, ", variance =", Qwen_UCD_ep_var)
print("Qwen_UCD Entity F1: mean =", Qwen_UCD_ef_mean, ", variance =", Qwen_UCD_ef_var)
print("Qwen_UCD Relation Recall: mean =", Qwen_UCD_rr_mean, ", variance =", Qwen_UCD_rr_var)
print("Qwen_UCD Relation Precision: mean =", Qwen_UCD_rp_mean, ", variance =", Qwen_UCD_rp_var)
print("Qwen_UCD Relation F1: mean =", Qwen_UCD_rf_mean, ", variance =", Qwen_UCD_rf_var)
# print("Qwen_UCD Relation Similarity: mean =", Qwen_UCD_rs_mean, ", variance =", Qwen_UCD_rs_var)

print("Qwen_single Entity Recall: mean =", Qwen_single_er_mean, ", variance =", Qwen_single_er_var)
print("Qwen_single Entity Precision: mean =", Qwen_single_ep_mean, ", variance =", Qwen_single_ep_var)
print("Qwen_single Entity F1: mean =", Qwen_single_ef_mean, ", variance =", Qwen_single_ef_var)
print("Qwen_single Relation Recall: mean =", Qwen_single_rr_mean, ", variance =", Qwen_single_rr_var)
print("Qwen_single Relation Precision: mean =", Qwen_single_rp_mean, ", variance =", Qwen_single_rp_var)
print("Qwen_single Relation F1: mean =", Qwen_single_rf_mean, ", variance =", Qwen_single_rf_var)
# print("Qwen_single Relation Similarity: mean =", Qwen_single_rs_mean, ", variance =", Qwen_single_rs_var)

print("DeepSeek_UCD Entity Recall: mean =", DeepSeek_UCD_er_mean, ", variance =", DeepSeek_UCD_er_var)
print("DeepSeek_UCD Entity Precision: mean =", DeepSeek_UCD_ep_mean, ", variance =", DeepSeek_UCD_ep_var)
print("DeepSeek_UCD Entity F1: mean =", DeepSeek_UCD_ef_mean, ", variance =", DeepSeek_UCD_ef_var)
print("DeepSeek_UCD Relation Recall: mean =", DeepSeek_UCD_rr_mean, ", variance =", DeepSeek_UCD_rr_var)
print("DeepSeek_UCD Relation Precision: mean =", DeepSeek_UCD_rp_mean, ", variance =", DeepSeek_UCD_rp_var)
print("DeepSeek_UCD Relation F1: mean =", DeepSeek_UCD_rf_mean, ", variance =", DeepSeek_UCD_rf_var)
# print("DeepSeek_UCD Relation Similarity: mean =", DeepSeek_UCD_rs_mean, ", variance =", DeepSeek_UCD_rs_var)

print("DeepSeek_single Entity Recall: mean =", DeepSeek_single_er_mean, ", variance =", DeepSeek_single_er_var)
print("DeepSeek_single Entity Precision: mean =", DeepSeek_single_ep_mean, ", variance =", DeepSeek_single_ep_var)
print("DeepSeek_single Entity F1: mean =", DeepSeek_single_ef_mean, ", variance =", DeepSeek_single_ef_var)
print("DeepSeek_single Relation Recall: mean =", DeepSeek_single_rr_mean, ", variance =", DeepSeek_single_rr_var)
print("DeepSeek_single Relation Precision: mean =", DeepSeek_single_rp_mean, ", variance =", DeepSeek_single_rp_var)
print("DeepSeek_single Relation F1: mean =", DeepSeek_single_rf_mean, ", variance =", DeepSeek_single_rf_var)
# print("DeepSeek_single Relation Similarity: mean =", DeepSeek_single_rs_mean, ", variance =", DeepSeek_single_rs_var)

print("GLM_UCD Entity Recall: mean =", GLM_UCD_er_mean, ", variance =", GLM_UCD_er_var)
print("GLM_UCD Entity Precision: mean =", GLM_UCD_ep_mean, ", variance =", GLM_UCD_ep_var)
print("GLM_UCD Entity F1: mean =", GLM_UCD_ef_mean, ", variance =", GLM_UCD_ef_var)
print("GLM_UCD Relation Recall: mean =", GLM_UCD_rr_mean, ", variance =", GLM_UCD_rr_var)
print("GLM_UCD Relation Precision: mean =", GLM_UCD_rp_mean, ", variance =", GLM_UCD_rp_var)
print("GLM_UCD Relation F1: mean =", GLM_UCD_rf_mean, ", variance =", GLM_UCD_rf_var)
# print("GLM_UCD Relation Similarity: mean =", GLM_UCD_rs_mean, ", variance =", GLM_UCD_rs_var)

print("GLM_single Entity Recall: mean =", GLM_single_er_mean, ", variance =", GLM_single_er_var)
print("GLM_single Entity Precision: mean =", GLM_single_ep_mean, ", variance =", GLM_single_ep_var)
print("GLM_single Entity F1: mean =", GLM_single_ef_mean, ", variance =", GLM_single_ef_var)
print("GLM_single Relation Recall: mean =", GLM_single_rr_mean, ", variance =", GLM_single_rr_var)
print("GLM_single Relation Precision: mean =", GLM_single_rp_mean, ", variance =", GLM_single_rp_var)
print("GLM_single Relation F1: mean =", GLM_single_rf_mean, ", variance =", GLM_single_rf_var)
# print("GLM_single Relation Similarity: mean =", GLM_single_rs_mean, ", variance =", GLM_single_rs_var)

# print("IT4RE Entity Recall: mean =", IT4RE_er_mean, ", variance =", IT4RE_er_var)
# print("IT4RE Entity Precision: mean =", IT4RE_ep_mean, ", variance =", IT4RE_ep_var)
# print("IT4RE Entity F1: mean =", IT4RE_ef_mean, ", variance =", IT4RE_ef_var)
# print("IT4RE Relation Similarity: mean =", IT4RE_rs_mean, ", variance =", IT4RE_rs_var)