import pandas as pd

file = 'students.csv';

df = pd.read_csv(file, sep=',')
print(df.shape)
print(df.columns)
print(df.dtypes)
print('\n')
print(df.describe()) #name and grade are strings
print('\n')
renamed_df = df.rename(columns={'score' : 'final_score','grade' : 'letter_grade'})
print(renamed_df)
print(renamed_df[['final_score', 'age', 'letter_grade']])
print('\n')
print(df.iloc[0:3])
print('\n')
print(df.loc[[1,3], ['name', 'grade'] ])
