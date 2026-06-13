Problem Statement
A school wants to simulate and store performance records for its students across three subjects. Your task is to generate this data using NumPy, manipulate the array, and save the records to a file.

Tasks
Task 1 — Generate and Inspect the Dataset Using NumPy random functions, create the following columns for 10 students: name (chosen randomly from a list of 5 names), age (random integers between 15 and 18), maths (random integers between 40 and 100), science (random integers between 40 and 100), and english (random integers between 40 and 100). Set np.random.seed(42) before generating any values. Print the shape of the marks array (only the three subject columns) and its dtype.

Task 2 — Reshape and Slice the Marks Array Take the marks array of shape (10, 3) and reshape it into shape (2, 5, 3). Print the reshaped array. Then, from the original (10, 3) marks array, slice and print the marks of the first five students for maths and science only (columns 0 and 1). In a comment, explain what the shape (2, 5, 3) represents in terms of the data.

Task 3 — Save the Records to a File Write all 10 student records to a text file called student_records.txt, with each record on its own line in the format: Name | Age | Maths | Science | English. Use the with statement to open the file. Print a confirmation message after writing. Then open the file in read mode and print all lines to verify the output.

Submission Guidelines
Use any online Python compiler without AI assistance.
Run your code fully, verify all outputs, then paste into the submission box.
Select Python as the language from the dropdown at the top.