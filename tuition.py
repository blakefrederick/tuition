import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

# https://open.canada.ca/data/en/dataset/b27148db-d7b4-4cef-b8d7-13cfc10487d5/resource/8cb16dec-5ff7-4eca-8562-835e876a918a
df = pd.read_csv('tuition-data.csv')

# Convert REF_DATE to the start year of the academic year
df['Year'] = df['REF_DATE'].apply(lambda x: int(x.split('/')[0]))

# Gotta be numeric
df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')

# No NaNs
df = df.dropna(subset=['VALUE'])

# Pivot!!
tuition_df = df.pivot_table(values='VALUE', index='Year', columns='GEO', aggfunc='mean')

# Time Series Analysis 
fig, ax = plt.subplots(figsize=(14,7))
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
for column in tuition_df.columns:
    ax.plot(tuition_df.index, tuition_df[column], label=column)
ax.set_xlabel('Academic Year Start')
ax.set_ylabel('Average Tuition Fees ($)')
ax.set_title('Average Tuition Fees Over Time by Province')
ax.legend()
plt.show()

# Heatmap time
plt.figure(figsize=(14,7))
sns.heatmap(tuition_df.transpose(), cmap='viridis', linecolor='white', linewidths=1)
plt.xlabel('Academic Year Start')
plt.ylabel('Province')
plt.title('Heatmap of Tuition Fees Over Time by Province ($)')
plt.show()

# Another heatmap, but this time to show percentage increases
tuition_increase = tuition_df.pct_change().fillna(0) * 100
tuition_increase = tuition_increase[tuition_increase.index > 2018]
tuition_increase.index = tuition_increase.index.astype(int)

plt.figure(figsize=(14, 10))
ax = sns.heatmap(tuition_increase.transpose(), cmap='coolwarm', annot=True, fmt='.1f', linewidths=.5)

# Get and set years as x
years = tuition_increase.index.tolist() 
ax.set_xticks(np.arange(len(years)))
ax.set_xticklabels(years, rotation=0)

plt.title('Percentage Increase in Tuition Fees Since 2019 by Province and Year')
plt.xlabel('Year')
plt.ylabel('Province')
plt.show()
