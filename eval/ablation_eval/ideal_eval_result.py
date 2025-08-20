import json
import statistics

# 初始化存储各指标值的列表
Qwen_wo_DM_entity_recall = []
Qwen_wo_DM_entity_precision = []
Qwen_wo_DM_entity_F1 = []
Qwen_wo_DM_relation_recall = []
Qwen_wo_DM_relation_precision = []
Qwen_wo_DM_relation_F1 = []

Qwen_wo_SR_entity_recall = []
Qwen_wo_SR_entity_precision = []
Qwen_wo_SR_entity_F1 = []
Qwen_wo_SR_relation_recall = []
Qwen_wo_SR_relation_precision = []
Qwen_wo_SR_relation_F1 = []



# 读取 JSONL 文件
file_path = 'ablation_eval_results.jsonl'
with open(file_path, 'r') as file:
    for line in file:
        # 解析每行的 JSON 数据
        data = json.loads(line)

        # 提取三个字段的数据
        Qwen_wo_DM = data['Qwen_wo_DM']
        Qwen_wo_SR = data['Qwen_wo_SR']

        # 将指标值添加到对应的列表中
        Qwen_wo_DM_entity_recall.append(Qwen_wo_DM['Entity Recall'])
        Qwen_wo_DM_entity_precision.append(Qwen_wo_DM['Entity Precision'])
        Qwen_wo_DM_entity_F1.append(Qwen_wo_DM['Entity F1'])
        Qwen_wo_DM_relation_recall.append(Qwen_wo_DM['Relation Recall'])
        Qwen_wo_DM_relation_precision.append(Qwen_wo_DM['Relation Precision'])
        Qwen_wo_DM_relation_F1.append(Qwen_wo_DM['Relation F1'])
        # Qwen_wo_DM_relation_similarity.append(Qwen_wo_DM['Relation Similarity'])

        Qwen_wo_SR_entity_recall.append(Qwen_wo_SR['Entity Recall'])
        Qwen_wo_SR_entity_precision.append(Qwen_wo_SR['Entity Precision'])
        Qwen_wo_SR_entity_F1.append(Qwen_wo_SR['Entity F1'])
        Qwen_wo_SR_relation_recall.append(Qwen_wo_SR['Relation Recall'])
        Qwen_wo_SR_relation_precision.append(Qwen_wo_SR['Relation Precision'])
        Qwen_wo_SR_relation_F1.append(Qwen_wo_SR['Relation F1'])
        # Qwen_wo_SR_relation_similarity.append(Qwen_wo_SR['Relation Similarity'])



# 计算均值和方差
Qwen_wo_DM_er_mean = statistics.mean(Qwen_wo_DM_entity_recall)
Qwen_wo_DM_er_var = statistics.variance(Qwen_wo_DM_entity_recall)
Qwen_wo_DM_ep_mean = statistics.mean(Qwen_wo_DM_entity_precision)
Qwen_wo_DM_ep_var = statistics.variance(Qwen_wo_DM_entity_precision)
Qwen_wo_DM_ef_mean = statistics.mean(Qwen_wo_DM_entity_F1)
Qwen_wo_DM_ef_var = statistics.variance(Qwen_wo_DM_entity_F1)
Qwen_wo_DM_rr_mean = statistics.mean(Qwen_wo_DM_relation_recall)
Qwen_wo_DM_rr_var = statistics.variance(Qwen_wo_DM_relation_recall)
Qwen_wo_DM_rp_mean = statistics.mean(Qwen_wo_DM_relation_precision)
Qwen_wo_DM_rp_var = statistics.variance(Qwen_wo_DM_relation_precision)
Qwen_wo_DM_rf_mean = statistics.mean(Qwen_wo_DM_relation_F1)
Qwen_wo_DM_rf_var = statistics.variance(Qwen_wo_DM_relation_F1)
# Qwen_wo_DM_rs_mean = statistics.mean(Qwen_wo_DM_relation_similarity)
# Qwen_wo_DM_rs_var = statistics.variance(Qwen_wo_DM_relation_similarity)

Qwen_wo_SR_er_mean = statistics.mean(Qwen_wo_SR_entity_recall)
Qwen_wo_SR_er_var = statistics.variance(Qwen_wo_SR_entity_recall)
Qwen_wo_SR_ep_mean = statistics.mean(Qwen_wo_SR_entity_precision)
Qwen_wo_SR_ep_var = statistics.variance(Qwen_wo_SR_entity_precision)
Qwen_wo_SR_ef_mean = statistics.mean(Qwen_wo_SR_entity_F1)
Qwen_wo_SR_ef_var = statistics.variance(Qwen_wo_SR_entity_F1)
Qwen_wo_SR_rr_mean = statistics.mean(Qwen_wo_SR_relation_recall)
Qwen_wo_SR_rr_var = statistics.variance(Qwen_wo_SR_relation_recall)
Qwen_wo_SR_rp_mean = statistics.mean(Qwen_wo_SR_relation_precision)
Qwen_wo_SR_rp_var = statistics.variance(Qwen_wo_SR_relation_precision)
Qwen_wo_SR_rf_mean = statistics.mean(Qwen_wo_SR_relation_F1)
Qwen_wo_SR_rf_var = statistics.variance(Qwen_wo_SR_relation_F1)
# Qwen_wo_SR_rs_mean = statistics.mean(Qwen_wo_SR_relation_similarity)
# Qwen_wo_SR_rs_var = statistics.variance(Qwen_wo_SR_relation_similarity)





# 打印结果
print("Qwen_wo_DM Entity Recall: mean =", Qwen_wo_DM_er_mean, ", variance =", Qwen_wo_DM_er_var)
print("Qwen_wo_DM Entity Precision: mean =", Qwen_wo_DM_ep_mean, ", variance =", Qwen_wo_DM_ep_var)
print("Qwen_wo_DM Entity F1: mean =", Qwen_wo_DM_ef_mean, ", variance =", Qwen_wo_DM_ef_var)
print("Qwen_wo_DM Relation Recall: mean =", Qwen_wo_DM_rr_mean, ", variance =", Qwen_wo_DM_rr_var)
print("Qwen_wo_DM Relation Precision: mean =", Qwen_wo_DM_rp_mean, ", variance =", Qwen_wo_DM_rp_var)
print("Qwen_wo_DM Relation F1: mean =", Qwen_wo_DM_rf_mean, ", variance =", Qwen_wo_DM_rf_var)
# print("Qwen_wo_DM Relation Similarity: mean =", Qwen_wo_DM_rs_mean, ", variance =", Qwen_wo_DM_rs_var)

print("Qwen_wo_SR Entity Recall: mean =", Qwen_wo_SR_er_mean, ", variance =", Qwen_wo_SR_er_var)
print("Qwen_wo_SR Entity Precision: mean =", Qwen_wo_SR_ep_mean, ", variance =", Qwen_wo_SR_ep_var)
print("Qwen_wo_SR Entity F1: mean =", Qwen_wo_SR_ef_mean, ", variance =", Qwen_wo_SR_ef_var)
print("Qwen_wo_SR Relation Recall: mean =", Qwen_wo_SR_rr_mean, ", variance =", Qwen_wo_SR_rr_var)
print("Qwen_wo_SR Relation Precision: mean =", Qwen_wo_SR_rp_mean, ", variance =", Qwen_wo_SR_rp_var)
print("Qwen_wo_SR Relation F1: mean =", Qwen_wo_SR_rf_mean, ", variance =", Qwen_wo_SR_rf_var)
# print("Qwen_wo_SR Relation Similarity: mean =", Qwen_wo_SR_rs_mean, ", variance =", Qwen_wo_SR_rs_var)

