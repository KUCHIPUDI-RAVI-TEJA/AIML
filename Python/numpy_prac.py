# import numpy as np

# arr = np.array([[1, 2, 3, 4],
#                 [5, 6, 7, 8],
#                 [9, 10, 11, 12]])
# print(arr[1:3, 0:2])
# print(arr[1:, :2])

#Task 1 

import numpy as np

np.random.seed(42)
names = ["Ravi", "Teja", "Pavan", "Kiran", "Ramesh"]
ages = [25, 26, 24, 23, 52]
size = 10
names_data = np.random.choice(names, size=size)
ages_data = np.random.choice(ages, size=size)
maths_data = np.random.randint(40, 100, size)
science_data = np.random.randint(40, 100, size)
english_data = np.random.randint(40, 100, size)

marks_array = np.array([maths_data, science_data, english_data]).T

print(marks_array)
print(f"Shape: {np.shape(marks_array)} \nDatatype: {marks_array.dtype}")

# Task 2
reshaped_marks_array = marks_array.reshape(2,5,3) # its a 3d array with 3 columns with 5 rows each in 2 blocks
print(reshaped_marks_array)

# first five students for maths and science 
math_science_of_first_five = marks_array[0:5, 0:2]
print(f"\nfirst five students marks for maths and science: \n{math_science_of_first_five}")

#Task 3
with open("student_records.txt", "w") as file:
    file.write("Name | Age | Maths | Science | English\n")
    for i in range(size):
        file.write(f"{names_data[i]} | {ages_data[i]} | {maths_data[i]} | {science_data[i]} | {english_data[i]}\n")
    
print("File Created\n")

with open("student_records.txt", "r") as file:
        for line in file:
            print(line)
    


print(np.__version__)