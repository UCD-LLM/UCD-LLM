import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 数据准备
methods = ['$Qwen$', '$UCD-LLM_{Qwen}$', '$DeepSeek$', '$UCD-LLM_{DeepSeek}$', '$GLM$', '$UCD-LLM_{GLM}$']
mef_means = [0.813, 0.906, 0.844, 0.883, 0.849, 0.898]
mef_stds = [0.175, 0.113, 0.181, 0.125, 0.150, 0.117]

# 创建增强型误差条形图
plt.figure(figsize=(14, 7), dpi=300)
sns.set(style="whitegrid", font_scale=1.2)
# palette = sns.color_palette("Blues_r", n_colors=len(methods))
custom_colors = ['#BAE3DC', '#8DD2C5', '#DAD7EA', '#BFBCDA', '#B3D1E7', '#7FB2D5']  # 示例颜色

# 主条形图
bars = plt.bar(methods, mef_means, yerr=mef_stds,
               capsize=10, alpha=0.85, color=custom_colors,
               error_kw=dict(elinewidth=2.5, ecolor='#979797', capthick=2))

# 添加性能提升箭头和标注
for i in range(0, len(methods), 2):
    if i + 1 < len(methods):  # 确保有对应的UCD-LLM变体
        base_val = mef_means[i]
        ucd_val = mef_means[i + 1]
        gain = ucd_val - base_val
        gain_percent = (gain / base_val) * 100

        # 添加提升箭头
        plt.annotate('',
                     xy=(i + 0.5, ucd_val+0.05),
                     xytext=(i + 0.5, base_val-0.05),
                     arrowprops=dict(arrowstyle='fancy,head_width=0.5,head_length=0.6',
                                     fc='#e74c3c', ec='#c0392b', lw=2))

        # 添加提升百分比标注
        plt.text(i + 0.5, (base_val + ucd_val) / 2 - 0.02,
                 f"+{gain_percent:.1f}%",
                 ha='center', va='center', fontsize=16, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', fc='#ffecb3', ec='#ff9800', alpha=0.9))

# 标注最优值
max_idx = np.argmax(mef_means)
plt.annotate(f'Optimal FEF: {mef_means[max_idx]:.3f}±{mef_stds[max_idx]:.3f}',
             xy=(max_idx, mef_means[max_idx]),
             xytext=(max_idx - 0.3, 1.1),
             arrowprops=dict(facecolor='#2c3e50', shrink=0.05, width=2),
             ha='center', fontsize=16, weight='bold',
             bbox=dict(boxstyle='round,pad=0.4', fc='#e3f2fd', ec='#0d47a1'))

# 添加稳定性标注
for i, std in enumerate(mef_stds):
    if i % 2 == 1:  # 只标注UCD-LLM变体的稳定性提升
        base_std = mef_stds[i - 1]
        std_reduction = ((base_std - std) / base_std) * 100
        plt.text(i, mef_means[i] + 0.02,
                 f"σ↓{std_reduction:.1f}%",
                 ha='center', fontsize=13,
                 bbox=dict(boxstyle='round,pad=0.2', fc='#c8e6c9', ec='#388e3c'))

# 添加基准线
plt.axhline(y=0.85, color='#7f8c8d', linestyle='--', alpha=0.7, lw=1.5)
# plt.text(len(methods) - 0.5, 0.7, 'High-Performance Threshold (0.85)',
#          fontsize=14, ha='right', va='bottom')

# 格式美化
plt.ylim(0, 1.2)
plt.ylabel('\nFunctional Entity F1-Score (FEF)\n', fontsize=16, fontweight='bold')
plt.xlabel('\n Models\n ', fontsize=16, fontweight='bold')
plt.title('\n',
           fontsize=18, pad=20, fontweight='bold')

# 添加网格增强可读性
plt.grid(axis='y', linestyle='--', alpha=0.4)

# 添加性能摘要
plt.text(0.5, 0.12,
         "UCD-LLM variants achieve significant FEF gains:\n"
         "$UCD-LLM_{Qwen}$: +11.4%  |  $UCD-LLM_{DeepSeek}$: +4.6%  |  $UCD-LLM_{GLM}$: +5.8%",
         fontsize=13,
         bbox=dict(boxstyle='round,pad=0.5', fc='#f5f5f5', ec='#616161', alpha=0.9))

plt.tight_layout()
plt.savefig('FEF_Comparison.png', bbox_inches='tight', dpi=300)
plt.show()