import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# 数据准备
models = ['$Qwen$', '$UCDLLM_Qwen$', '$DeepSeek$', '$UCDLLM_DeepSeek$', '$GLM$', '$UCDLLM_GLM$']
mef = [0.8129, 0.9056, 0.8440, 0.8825, 0.8493, 0.8978]
rnf = [0.5959, 0.6928, 0.6104, 0.6446, 0.6238, 0.6699]
mer = [0.776, 0.9095, 0.8077, 0.8876, 0.8261, 0.9037]
rnr = [0.5432, 0.6688, 0.5342, 0.6706, 0.5548, 0.6842]

# 创建雷达图与散点图组合
plt.figure(figsize=(8, 6), dpi=300)  # Adjusted figure size for single subplot
plt.rcParams['font.family'] = 'Times New Roman'  # 设置字体族
# gs = GridSpec(1, 2, width_ratios=[1, 1.2])  # Removed as we only need one subplot

# 子图1：元素vs关系F1对比雷达图
ax1 = plt.subplot(111, polar=True)  # Using single subplot

# 修复1：正确设置雷达图轴数（3个模型类别）
angles = np.linspace(0, 2 * np.pi, 3, endpoint=False).tolist()
angles += angles[:1]  # 闭合

# UCD-LLM变体数据（取Qwen/DeepSeek/GLM对应的UCD变体）
ucd_mef = [mef[1], mef[3], mef[5], mef[1]]  # 闭合循环
ucd_rnf = [rnf[1], rnf[3], rnf[5], rnf[1]]  # 闭合循环

ax1.plot(angles, ucd_mef, 'o-', linewidth=2, label='Functional Entity F1-Score (FEF)',
         color='#3498db', markersize=8)
ax1.fill(angles, ucd_mef, alpha=0.1, color='#3498db')
ax1.plot(angles, ucd_rnf, 's-', linewidth=2, label='Relation Network F1-Score (RNF)',
         color='#e74c3c', markersize=8)
ax1.fill(angles, ucd_rnf, alpha=0.1, color='#e74c3c')

# 基础模型数据
base_mef = [mef[0], mef[2], mef[4], mef[0]]  # 闭合循环
base_rnf = [rnf[0], rnf[2], rnf[4], rnf[0]]  # 闭合循环
ax1.plot(angles, base_mef, 'o--', linewidth=1, color='#2980b9', alpha=0.6)
ax1.plot(angles, base_rnf, 's--', linewidth=1, color='#c0392b', alpha=0.6)

# 雷达图美化
ax1.set_xticks(angles[:-1])
ax1.set_xticklabels(['$\ Qwen\ $', '$\ DeepSeek\ $', '$\ GLM\ $'], fontsize=14, fontweight='bold')
ax1.set_rlabel_position(30)
ax1.set_yticks([0.6, 0.7, 0.8, 0.9])
ax1.set_yticklabels(['0.6', '0.7', '0.8', '0.9'], fontsize=14)
ax1.set_ylim(0.5, 0.95)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(loc='right', bbox_to_anchor=(1.0, 1.1))
# ax1.set_title('UCD-LLM vs Base Models: Element & Relation F1 Comparison', pad=20)

plt.tight_layout()
plt.savefig('radar_chart.png', bbox_inches='tight')
plt.show()