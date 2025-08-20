import json
import statistics
import matplotlib.pyplot as plt
import numpy as np

def preprocess(json_data):
    # 初始化实体和关系字典
    entity_num = 0
    relation_num = 0

    # 添加参与者实体
    for actor in json_data['actors']:
        entity_num += 1

    # 添加用例实体
    for usecase in json_data['usecases']:
        entity_num += 1

    # 添加关联关系
    for actor, usecases in json_data['association_relationships'].items():
        for usecase in usecases:
            relation_num += 1

    # 添加包含关系
    for usecase, included_usecases in json_data['inclusion_relationships'].items():
        for included_usecase in included_usecases:
            relation_num += 1

    # 添加扩展关系
    for usecase, extended_usecases in json_data['extension_relationships'].items():
        for extended_usecase in extended_usecases:
            relation_num += 1

    # 添加用例间泛化关系
    for general_usecase, specific_usecases in json_data['generalization_relationships_for_usecases'].items():
        for specific_usecase in specific_usecases:
            relation_num += 1

    # 添加参与者泛化关系
    for general_actor, specific_actors in json_data['generalization_relationships_for_actors'].items():
        for specific_actor in specific_actors:
            relation_num += 1

    return entity_num, relation_num


elements = []
relationships = []
for i in range(1,61):
    lower = ((i - 1) // 10) * 10 + 1
    upper = lower + 9
    # Read clean data
    clean_file = f"../datasets/60_ideal_UCD/{lower}-{upper}/{i}_result.json"
    with open(clean_file, "r") as f1:
        data_clean = json.load(f1)
    en, re = preprocess(data_clean)
    elements.append(en)
    relationships.append(re)
print(elements)
print(relationships)
# 计算统计量
en_mean = np.mean(elements)
re_mean = np.mean(relationships)
en_median = np.median(elements)
re_median = np.median(relationships)

# 创建图形
plt.figure(figsize=(10, 8))
plt.rcParams['font.family'] = 'Times New Roman'  # 设置字体族

# 定义颜色方案 - 两个类别使用不同色系
# 第一个类别（Elements）：蓝色系
color1_violin = '#FAE5DC'    # 小提琴图背景色
color1_box_fill = '#F3CCBB'  # 箱线图填充色（稍深）
color1_box_edge = '#E29C82'  # 箱线图描边色（更深）

# 第二个类别（Relationships）：绿色系
color2_violin = '#E0ECEC'    # 小提琴图背景色
color2_box_fill = '#C2DADA'  # 箱线图填充色（稍深）
color2_box_edge = '#8DB9B6'  # 箱线图描边色（更深）

# 1. 小提琴图 (Violin plots)
violin_parts = plt.violinplot([elements, relationships], positions=[1, 2], showmeans=False, showmedians=False)
# 为每个小提琴图设置不同颜色
violin_parts['bodies'][0].set_facecolor(color1_violin)
violin_parts['bodies'][0].set_alpha(0.3)
violin_parts['bodies'][1].set_facecolor(color2_violin)
violin_parts['bodies'][1].set_alpha(0.3)

# 设置小提琴图竖线颜色与对应箱线图描边色一致
violin_parts['cbars'].set_color([color1_box_edge, color2_box_edge])  # 中间线
violin_parts['cmaxes'].set_color([color1_box_edge, color2_box_edge]) # 顶部线
violin_parts['cmins'].set_color([color1_box_edge, color2_box_edge])  # 底部线

# 2. 箱线图 (Box plots)
# 设置箱线图公共属性（中位线暂时不指定颜色）
medianprops = dict(linestyle='-', linewidth=2.5)  # 中位数线属性
whiskerprops = dict(linewidth=1.5)  # 须线属性（暂不设置颜色）
capprops = dict(linewidth=1.5)      # 顶部和底部横线属性（暂不设置颜色）

# 绘制箱线图
box = plt.boxplot(
    [elements, relationships],
    positions=[1, 2],
    widths=0.15,
    patch_artist=True,  # 允许填充颜色
    medianprops=medianprops,
    whiskerprops=whiskerprops,
    capprops=capprops
)

# 为第一个箱线图设置样式（填充色、边框色、须线色、顶底横线色和中位线色）
box['boxes'][0].set_facecolor(color1_box_fill)
box['boxes'][0].set_edgecolor(color1_box_edge)
box['boxes'][0].set_alpha(0.9)
for whisker in box['whiskers'][0:2]:  # 前两个须线属于第一个箱线图
    whisker.set_color(color1_box_edge)
for cap in box['caps'][0:2]:  # 前两个顶底横线属于第一个箱线图
    cap.set_color(color1_box_edge)
box['medians'][0].set_color(color1_box_edge)  # 第一个箱线图的中位线

# 为第二个箱线图设置样式
box['boxes'][1].set_facecolor(color2_box_fill)
box['boxes'][1].set_edgecolor(color2_box_edge)
box['boxes'][1].set_alpha(0.9)
for whisker in box['whiskers'][2:4]:  # 后两个须线属于第二个箱线图
    whisker.set_color(color2_box_edge)
for cap in box['caps'][2:4]:  # 后两个顶底横线属于第二个箱线图
    cap.set_color(color2_box_edge)
box['medians'][1].set_color(color2_box_edge)  # 第二个箱线图的中位线
# 3. 散点图 (Scatter plots with jitter)
def jitter(arr, position, scale=0.05):
    jittered = position + np.random.normal(scale=scale, size=len(arr))
    return jittered

# 为散点添加抖动避免重叠
x_elements = jitter(elements, 1, 0.04)
x_relationships = jitter(relationships, 2, 0.04)

# 绘制散点图，使用与小提琴图相同的色系
plt.scatter(x_elements, elements, s=70, alpha=0.7, color=color1_violin,
           edgecolor='white', linewidth=0.7, label='Data Points (Entities)')
plt.scatter(x_relationships, relationships, s=70, alpha=0.7, color=color2_violin,
           edgecolor='white', linewidth=0.7, label='Data Points (Relationships)')

# 4. 添加均值和中位数标记
plt.scatter([1], [en_mean], s=150, marker='D', color='gold',
            zorder=10, label=f'Mean: {en_mean:.1f}')
plt.scatter([1], [en_median], s=150, marker='s', color='#A59ACA',
            zorder=10, label=f'Median: {en_median:.1f}')
plt.scatter([2], [re_mean], s=150, marker='D', color='gold', zorder=10)
plt.scatter([2], [re_median], s=150, marker='s', color='#A59ACA', zorder=10)

# 添加统计值文本
plt.text(1.15, en_mean+0.5, f'Mean: {en_mean:.1f}', fontsize=16, fontweight='bold')
plt.text(1.15, en_median-0.7, f'Median: {en_median:.1f}', fontsize=16, fontweight='bold')
plt.text(2.15, re_mean+0.5, f'Mean: {re_mean:.1f}', fontsize=16, fontweight='bold')
plt.text(2.15, re_median-0.7, f'Median: {re_median:.1f}', fontsize=16, fontweight='bold')

# 添加标题和标签
# plt.title('Raincloud Plot of Modeling Elements and Relationships in Use Case Diagrams',
#           fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Category', fontsize=18, fontweight='bold')
plt.ylabel('Quantity', fontsize=18, fontweight='bold')
plt.xticks([1, 2], ['Functional Entities', 'Relationships'], fontsize=18, weight='bold')
plt.ylim(0, 40)  # 设置Y轴范围

# 添加图例
handles, labels = plt.gca().get_legend_handles_labels()
# 创建自定义图例项
from matplotlib.lines import Line2D
custom_lines = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=color1_violin, markersize=10),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=color2_violin, markersize=10),
    Line2D([0], [0], marker='D', color='w', markerfacecolor='gold', markersize=10,),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='#A59ACA', markersize=10, )
]
plt.legend(custom_lines, ['Entity Data Points', 'Relationship Data Points', 'Mean Value', 'Median Value'],
           loc='upper right', frameon=True, framealpha=0.9)

# # 添加数据点计数
# plt.text(0.92, -3, f'n = {len(elements)}', fontsize=14)
# plt.text(1.92, -3, f'n = {len(relationships)}', fontsize=14)

# 添加网格线
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('UCD_Statistics_Distribution.png', dpi=300, bbox_inches='tight')
plt.show()