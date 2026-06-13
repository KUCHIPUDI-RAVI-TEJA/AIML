
import seaborn as sns

df = sns.load_dataset('titanic')

# filter_condition = (df['sex'] == 'female') & (df['pclass'].isin([1,2]))

# filtered_df = df[filter_condition].fillna({'age':30}).sort_values(['fare'], ascending=False).sort_index()

# filtered_df['fare_group'] = 'high'


# filtered_df.to_csv('female_upper_class')

result = df.groupby('pclass').agg(
    total_passengers=('survived', 'count'),
    survivors=('survived', 'sum'),
    survival_rate=('survived', 'mean')
).reset_index()

print(result)
