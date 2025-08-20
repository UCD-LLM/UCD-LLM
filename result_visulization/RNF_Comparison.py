import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 数据准备
methods = ['$Qwen$', '$UCD-LLM_{Qwen}$', '$DeepSeek$', '$UCD-LLM_{DeepSeek}$', '$GLM$', '$UCD-LLM_{GLM}$']
rnf_means = [0.596, 0.693, 0.610, 0.645, 0.624, 0.670]
rnf_stds = [0.233, 0.174, 0.201, 0.192, 0.207, 0.191]

# 创建增强型误差条形图
plt.figure(figsize=(14, 7), dpi=300)
sns.set(style="whitegrid", font_scale=1.2)
palette = sns.color_palette("Blues_r", n_colors=len(methods))
custom_colors = ['#F5D9E6', '#E1B6B5', '#F9F2C1', '#F5E09B', '#EDF4F5', '#C5E3E2',]  # 示例颜色

# 主条形图
bars = plt.bar(methods, rnf_means, yerr=rnf_stds,
               capsize=10, alpha=0.85, color=custom_colors,
               error_kw=dict(elinewidth=2.5, ecolor='#979797', capthick=2))

# 添加性能提升箭头和标注
for i in range(0, len(methods), 2):
    if i + 1 < len(methods):  # 确保有对应的UCD-LLM变体
        base_val = rnf_means[i]
        ucd_val = rnf_means[i + 1]
        gain = ucd_val - base_val
        gain_percent = (gain / base_val) * 100

        # 添加提升箭头
        plt.annotate('',
                     xy=(i + 0.5, ucd_val+0.05),
                     xytext=(i + 0.5, base_val-0.05),
                     arrowprops=dict(arrowstyle='fancy,head_width=0.5,head_length=0.6',
                                     fc='#e74c3c', ec='#c0392b', lw=2))

        # 添加提升百分比标注
        plt.text(i + 0.5, (base_val + ucd_val) / 2 - 0.01,
                 f"+{gain_percent:.1f}%",
                 ha='center', va='center', fontsize=16, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', fc='#ffecb3', ec='#ff9800', alpha=0.9))

# 标注最优值
max_idx = np.argmax(rnf_means)
plt.annotate(f'Optimal RNF: {rnf_means[max_idx]:.3f}±{rnf_stds[max_idx]:.3f}',
             xy=(max_idx, rnf_means[max_idx]),
             xytext=(max_idx - 0.3, 0.9),
             arrowprops=dict(facecolor='#2c3e50', shrink=0.05, width=2),
             ha='center', fontsize=16, weight='bold',
             bbox=dict(boxstyle='round,pad=0.4', fc='#e3f2fd', ec='#0d47a1'))

# 添加稳定性标注
for i, std in enumerate(rnf_stds):
    if i % 2 == 1:  # 只标注UCD-LLM变体的稳定性提升
        base_std = rnf_stds[i - 1]
        std_reduction = ((base_std - std) / base_std) * 100
        plt.text(i, rnf_means[i] + 0.01,
                 f"σ↓{std_reduction:.1f}%",
                 ha='center', fontsize=13,
                 bbox=dict(boxstyle='round,pad=0.2', fc='#c8e6c9', ec='#388e3c'))

# 添加基准线
plt.axhline(y=0.65, color='#7f8c8d', linestyle='--', alpha=0.7, lw=1.5)
# plt.text(len(methods) - 0.5, 0.652, 'Performance Threshold (0.65)',
#          fontsize=14, ha='right', va='bottom')

# 格式美化
plt.ylim(0, 1)
plt.ylabel('\n Relation Network F1-Score (RNF)\n ', fontsize=16, fontweight='bold')
plt.xlabel('\n Models\n ', fontsize=16, fontweight='bold')
plt.title('\n',
          fontsize=18, pad=20, fontweight='bold')

# 添加网格增强可读性
plt.grid(axis='y', linestyle='--', alpha=0.4)

# 添加性能摘要
plt.text(0.5, 0.12,
         "UCD-LLM variants achieve significant RNF gains:\n"
         "$UCD-LLM_{Qwen}$: +16.3%  |  $UCD-LLM_{DeepSeek}$: +5.7%  |  $UCD-LLM_{GLM}$: +7.4%",
         fontsize=13,
         bbox=dict(boxstyle='round,pad=0.5', fc='#f5f5f5', ec='#616161', alpha=0.9))

# # 添加关系提取挑战说明
# plt.text(3.5, 0.15,
#          "Relation extraction is more challenging than element extraction\n"
#          "due to complex dependencies and semantic variations",
#          fontsize=14, ha='center',
#          bbox=dict(boxstyle='round,pad=0.5', fc='#fbe9e7', ec='#ff5722', alpha=0.7))

plt.tight_layout()
plt.savefig('RNF_Comparison.png', bbox_inches='tight', dpi=300)
plt.show()