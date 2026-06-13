import pandas as pd
import io

dt = '''name,sex,age,pclass,survived
Asha,female,34.0,1,1
Ravi,male,,3,0
Meera,female,28.0,2,1
Kabir,male,45.0,1,0
Neha,female,,2,1
Arjun,male,52.0,3,1
Priya,female,31.0,2,1
Vikram,male,29.0,1,0
'''

#Build the DataFrame from the inline CSV text above (you may use pd.read_csv(io.StringIO(...)) or build it from a dictionary of lists).
df = pd.read_csv(io.StringIO(dt))
print(df)
print('\n')

#Report the count of missing values per column.
print(df.isnull().sum())
print('\n')

#Replace missing age values with 0 using the fillna approach.
update_df = df.fillna({"age": 0})
print(update_df)
print('\n')

#Filter the DataFrame to passengers who survived (survived == 1) AND have age > 30. Use the bitwise AND with parentheses around each condition.
#Sort the filtered result by age in descending order and reset the index.
#Print the final filtered, sorted DataFrame.
filtered_df = update_df[(update_df['survived'] == 1) & (update_df['age'] > 30)].sort_values(['age'], ascending=False).reset_index()
print(filtered_df)
print('\n')



