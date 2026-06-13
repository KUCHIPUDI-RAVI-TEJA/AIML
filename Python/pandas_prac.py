import numpy as np
import pandas as pd

# student_data = np.array([["Alice", 20, 88.5, "A"],
#                           ["Bob",   19, 73.0, "B"]])
# print(student_data.dtype) 

# print(pd.__version__)   # 2.2.2

# scores = pd.Series([88.5, 73.0, 91.0, 65.5])
# print(scores)

# scores2 = pd.Series(data = [88.5, 73.0, 91.0, 65.5], index=["Alice", "Bob", "Charlie", "Diana"])
# print(scores2)
# print(scores2['Diana'])
# # print(scores2[3])
# print(scores2.values)
# print(scores2.index)

# data = {"Alice": 88.5, "Bob": 73.0, "Charlie": 91.0}
# scores = pd.Series(data)
# print(scores.values)   # numpy array: [88.5 73.0 91.0]
# print(scores.index)    # Index(['Alice', 'Bob', 'Charlie'])
# print(scores.values.dtype)

# data = {
#     "name":  ["Alice", "Bob", "Charlie", "Diana"],
#     "age":   [20, 19, 20, 20],
#     "score": [88.5, 73.0, 91.0, 65.5],
#     "grade": ["A", "B", "A", "B"]
# }
# df = pd.DataFrame(data)
# print(df)

# rows = [
#     {"name": "Alice", "age": 20, "score": 88.5},
#     {"name": "Bob",   "age": 19, "score": 73.0},
# ]
# df = pd.DataFrame(rows)

# array = np.array([[20, 88.5], [19, 73.0]])
# # print(array)
# df = pd.DataFrame(array, columns=["age", "score"], index=['p1', 'p2'])
# # print(df)
# print(df.dtypes)


# import seaborn as sns
# titanic = sns.load_dataset("titanic")
# print(titanic.shape)
# print(titanic.head())
# print(titanic.tail())
# print(titanic.columns)
# print(titanic.index)
# print(titanic.info)
# print(titanic.describe())
# print(titanic['age'])
# titanic_renamed = titanic.rename(columns={
#     "pclass":  "ticket_class",
#     "sibsp":   "siblings_spouses",
#     "parch":   "parents_children"
# })
# print(titanic_renamed.columns)

# print(titanic.iloc[0])    # first row
# print(titanic.iloc[80])   # row at integer position 80
# print(titanic.iloc[-1])   # last row (negative indexing)

# print(titanic.iloc[0:5, 1:4])   # rows 0-4, columns 1, 2, 3

# print(type(titanic))
# survivors = titanic[titanic["survived"] == 1]

# # iloc[0] returns the FIRST row of survivors (virtual position 0)
# print(survivors.iloc[0])
# print(survivors.iloc[1])
# # # loc[0] throws a KeyError because index label 0 may not exist in survivors
# print(survivors.loc[1])   # error if no row has label 0

# print(titanic.loc[0:4, "age"])

# titanic_renamed = titanic.rename(columns={'pclass': 'ticket_class', 'sibsp': 'siblings_spouses'})
# print(titanic.columns)

# Approach 1
# result1 = titanic['age']

# # Approach 2
# result2 = titanic[['age', 'pclass']]

# print(result1.dtypes)
# print(result2.dtypes)

# print(titanic.shape)
# condition = (titanic['pclass'] == 1) & (titanic['sex'] == 'female')
# tit = titanic[condition]
# print(tit.shape)

# print(titanic[titanic['pclass'].isin([1, 2])])

# print(titanic[titanic['embark_town'].str.contains('South')])

# print(titanic.sort_values(['pclass', 'age'], ascending=[True, False], na_position='last'))

# sorted_df = titanic.sort_values('age')
# print(sorted_df)
# sorted_df = sorted_df.reset_index()
# print(sorted_df)

# sorted_df.loc[0, 'age'] = 0.43

# print('\n')
# print(sorted_df)

# titanic['Balaji_col'] = titanic['age']
# print(titanic)

# print(titanic.isna().sum() )
# cleaned_df = titanic.fillna({'age': 0, 'embarked': 'unknown'})
# print(cleaned_df.isna().sum() )

# titanic.dropna(subset=['age'])

# print(titanic['sex'] == 'female')

# print(titanic.groupby('pclass').mean(numeric_only=True))

# result = titanic.groupby('region').agg({
#     'sales': ['sum', 'mean'],
#     'quantity': ['sum', 'max']
# })

# print(titanic.groupby(['age', 'pclass'])['survived'].mean())
# print('\n')
# print(titanic.groupby(['pclass', 'age'])['survived'].mean())









import seaborn as sns
titanic = sns.load_dataset("titanic")

print(titanic.head())
print(titanic.describe())
print(titanic.info())

summary = titanic.groupby(['pclass', 'sex']).agg(
    total_passengers=('survived', 'count'),
    survivors =('survived', 'sum'),
    survival_rate =('survived', 'mean'),
    avg_age =('age', 'mean'),
    max_fare  =('fare', 'max'),
)

print(summary)