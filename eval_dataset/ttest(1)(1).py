import pandas as pd
from scipy.stats import ttest_ind
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = "/home/szy/proj/crf/LCK_VS_anal/dockingscore.xlsx"  # 调整xlsx文件路径
dockingscore_data = pd.read_excel(file_path)

# Split data into active and inactive
active_data = dockingscore_data[dockingscore_data['Name'].str.startswith('CHEMBL')]  #active_data 开头是 CHEMBL，name是表头，根据自己的修改
inactive_data = dockingscore_data[dockingscore_data['Name'].str.startswith('C') & ~dockingscore_data['Name'].str.startswith('CHEMBL')] #inactive 开头是C但不是CHEMBL


# Perform t-test and store results
ttest_results = {}
for software in ['Vina', 'PLANET', 'Autodock-gpu']:  #根据筛选软件改名称，根据excel文件表头修改
    t_stat, p_val = ttest_ind(active_data[software], inactive_data[software])
    ttest_results[software] = f"{software}: t-statistic = {t_stat:.2f}, p-value = {format(p_val, '.5e')}"
    print(ttest_results[software])

# Define contrasting colors and line styles for the ROC curves
colors = { 
    'Vina': 'blue',   #根据筛选软件修改名称，根据excel写的修改
    'PLANET': 'green',
    'Autodock-gpu': 'red'
}
line_styles = {
    'Vina': '--',   #同上修改方式
    'PLANET': '-',
    'Autodock-gpu': '-.'
}

# Generate ROC curves
dockingscore_data['Label'] = dockingscore_data['Name'].apply(lambda x: 1 if x.startswith('CHEMBL') else 0)  #NAME根据表头修改
plt.figure(figsize=(10, 7))
for software in colors.keys():
    fpr, tpr, _ = roc_curve(dockingscore_data['Label'], -dockingscore_data[software])  # Negative scores since lower docking scores usually indicate better binding
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, color=colors[software], linestyle=line_styles[software], label=f'{software} (AUC = {roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier (AUC = 0.50)')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves for Docking Software with Contrasting Colors and Line Styles')
plt.legend(loc="lower right")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Boxplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, software in zip(axes, ['Vina', 'PLANET', 'Autodock-gpu']):  #参考上面软件修改方式修改
    sns.boxplot(x=dockingscore_data['Label'], y=dockingscore_data[software], ax=ax, palette="Set2")
    ax.set_title(f'Boxplot for {software}')
    ax.set_xlabel('Activity')
    ax.set_xticklabels(['Inactive', 'Active'])
    ax.set_ylabel('Docking Score')
    # Add t-test results to the plot
    ax.text(0.5, -0.15, ttest_results[software], horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=10, color='black')
plt.tight_layout()
plt.show()

# Violin plots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, software in zip(axes, ['Vina', 'PLANET', 'Autodock-gpu']): #参考上面软件修改方式修改
    sns.violinplot(x=dockingscore_data['Label'], y=dockingscore_data[software], ax=ax, palette="Set2", inner="quartile")
    ax.set_title(f'Violin plot for {software}')
    ax.set_xlabel('Activity')
    ax.set_xticklabels(['Inactive', 'Active'])
    ax.set_ylabel('Docking Score')
    # Add t-test results to the plot
    ax.text(0.5, -0.15, ttest_results[software], horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=10, color='black')
plt.tight_layout()
plt.show()
