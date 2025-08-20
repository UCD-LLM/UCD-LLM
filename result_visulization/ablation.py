import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap

# 数据准备
models = ['UCD-LLM', 'w/o DM', 'w/o SR']
entity_data = {
    'FER': [0.9241, 0.9011, 0.9136],
    'FEP': [0.9095, 0.9153, 0.8953],
    'FEF': [0.9056, 0.8958, 0.8918]
}
relation_data = {
    'RNR': [0.7469, 0.6960, 0.6856],
    'RNP': [0.6688, 0.5359, 0.6862],
    'RNF': [0.6928, 0.5838, 0.6693]
}

# 创建对比图表
plt.figure(figsize=(16, 10), dpi=300)
plt.rcParams['font.family'] = 'Times New Roman'  # 设置字体族
# 修改网格布局：2行3列，底部行宽度比例为1:0.1:1
gs = GridSpec(2, 3, width_ratios=[1, 0.1, 1], height_ratios=[1.1, 1.1])

# 子图1：实体指标对比
ax1 = plt.subplot(gs[0, 0])
bar_width = 0.25
x = np.arange(len(models))
colors = ['#B9A8C2', '#E3D8D9', '#B0BBCB']

# 绘制实体指标
for i, (metric, values) in enumerate(entity_data.items()):
    ax1.bar(x + i*bar_width, values, width=bar_width,
            label=metric, color=colors[i], alpha=0.85,
            edgecolor='none', linewidth=1.2)

# 添加数值标注
for i, model in enumerate(models):
    for j, metric in enumerate(entity_data.keys()):
        height = entity_data[metric][i]
        ax1.text(x[i] + j*bar_width, height+0.001, f'{height:.4f}',
                ha='center', va='bottom', fontsize=12)

# 子图美化
ax1.set_xticks(x + bar_width)
ax1.set_xticklabels(models, fontsize=14, weight='bold')
ax1.set_ylim(0.88, 0.935)
ax1.set_ylabel('Score', fontsize=14, weight='bold')
ax1.set_title('Functional Entity Extraction Performance Impact', fontsize=18, pad=15, weight='bold')
ax1.legend(loc='upper right', frameon=True)
ax1.grid(axis='y', linestyle='--', alpha=0.4)

# 子图2：关系指标对比
ax2 = plt.subplot(gs[0, 2])
# 绘制关系指标
for i, (metric, values) in enumerate(relation_data.items()):
    ax2.bar(x + i*bar_width, values, width=bar_width,
            label=metric, color=colors[i], alpha=0.85,
            edgecolor='none', linewidth=1.2)

# 添加数值标注
for i, model in enumerate(models):
    for j, metric in enumerate(relation_data.keys()):
        height = relation_data[metric][i]
        ax2.text(x[i] + j*bar_width, height+0.005, f'{height:.4f}',
                ha='center', va='bottom', fontsize=12)

# 子图美化
ax2.set_xticks(x + bar_width)
ax2.set_xticklabels(models, fontsize=14, weight='bold')
ax2.set_ylim(0.50, 0.78)
ax2.set_ylabel('Score', fontsize=14, weight='bold')
ax2.set_title('Relation Network Extraction Performance Impact', fontsize=18, pad=15, weight='bold')
ax2.legend(loc='upper right', frameon=True)
ax2.grid(axis='y', linestyle='--', alpha=0.4)

# 计算性能降幅百分比
entity_impact = {
    'Recall': [0, -2.5, -1.1],
    'Precision': [0, +0.6, -1.6],
    'F1': [0, -1.1, -1.5]
}
relation_impact = {
    'Recall': [0, -6.8, -8.2],
    'Precision': [0, -19.8, +2.6],
    'F1': [0, -15.7, -3.4]
}

# 创建热力图数据
heatmap_data = np.array([
    [0, -2.5, -1.1, 0, -6.8, -8.2],
    [0, +0.6, -1.6, 0, -19.8, +2.6],
    [0, -1.1, -1.5, 0, -15.7, -3.4]
])

# 拆分热力图数据
entity_heatmap = heatmap_data[:, :3]  # 前三列是实体数据
relation_heatmap = heatmap_data[:, 3:]  # 后三列是关系数据


# colors = ['#A9A3CA', '#B9B3D8', '#D6D4EA',  '#F1EFF7']
colors = ['#815C94', '#FFFFFF']
n_bins = 100  # 颜色过渡的细腻程度
custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=n_bins)

# 子图3：实体机制功效热力图 (左侧)
ax3_entity = plt.subplot(gs[1, 0])
# 使用自定义颜色映射
im_entity = ax3_entity.imshow(entity_heatmap, cmap=custom_cmap, vmin=-20, vmax=5, aspect='auto')

# 添加数值标注
for i in range(entity_heatmap.shape[0]):
    for j in range(entity_heatmap.shape[1]):
        color = 'black' if abs(entity_heatmap[i, j]) < 10 else 'white'
        ax3_entity.text(j, i, f'{entity_heatmap[i, j]:.1f}%',
                ha='center', va='center', color=color, fontsize=13, weight='bold')

# 设置坐标轴
ax3_entity.set_xticks(np.arange(3))
ax3_entity.set_xticklabels(['UCD-LLM', 'w/o DM', 'w/o SR'], fontsize=14, weight='bold')
ax3_entity.set_yticks(np.arange(3))
ax3_entity.set_yticklabels(['FER', 'FEP', 'FEF'], fontsize=14, weight='bold')

# 添加分隔线
ax3_entity.axvline(x=0.5, color='white', linestyle='-', alpha=0.7)
ax3_entity.axvline(x=1.5, color='white', linestyle='-', alpha=0.7)
ax3_entity.axhline(y=0.5, color='white', linestyle='-', alpha=0.7)
ax3_entity.axhline(y=1.5, color='white', linestyle='-', alpha=0.7)

# 子图4：关系机制功效热力图 (右侧)
ax3_relation = plt.subplot(gs[1, 2])
# 使用自定义颜色映射
im_relation = ax3_relation.imshow(relation_heatmap, cmap=custom_cmap, vmin=-20, vmax=5, aspect='auto')

# 添加数值标注
for i in range(relation_heatmap.shape[0]):
    for j in range(relation_heatmap.shape[1]):
        color = 'black' if abs(relation_heatmap[i, j]) < 10 else 'white'
        ax3_relation.text(j, i, f'{relation_heatmap[i, j]:.1f}%',
                ha='center', va='center', color=color, fontsize=13, weight='bold')

# 设置坐标轴
ax3_relation.set_xticks(np.arange(3))
ax3_relation.set_xticklabels(['UCD-LLM', 'w/o DM', 'w/o SR'], fontsize=14, weight='bold')
ax3_relation.set_yticks(np.arange(3))
ax3_relation.set_yticklabels(['RNR', 'RNP', 'RNF'], fontsize=14, weight='bold')

# 添加分隔线
ax3_relation.axvline(x=0.5, color='white', linestyle='-', alpha=0.7)
ax3_relation.axvline(x=1.5, color='white', linestyle='-', alpha=0.7)
ax3_relation.axhline(y=0.5, color='white', linestyle='-', alpha=0.7)
ax3_relation.axhline(y=1.5, color='white', linestyle='-', alpha=0.7)

# 在中间位置添加颜色条 (图例)
cax = plt.subplot(gs[1, 1])
cbar = plt.colorbar(im_entity, cax=cax)
cbar.set_label('Performance Change (%)', fontsize=13)
cax.set_axis_off()  # 隐藏坐标轴，只保留颜色条

plt.tight_layout()
plt.subplots_adjust(bottom=0.05, top=0.92, hspace=0.12)  # hspace从0.25减小到0.08，显著缩小间距
plt.savefig('ablation.png', dpi=300, bbox_inches='tight')
plt.show()
