Problem Statement
You are building a small data utility that demonstrates your understanding of JSON structure, validation, serialisation, and parsing in Python.

Tasks
Task 1 — Create and Serialise a Nested JSON Object Create a Python dictionary representing a student with keys: name, age, passed (boolean), marks (list of three numbers), and a nested address object containing city and pincode. Convert it to a formatted JSON string using json.dumps() with indent=4 and print the result.

Task 2 — Parse JSON and Access Values Using json.loads(), parse the JSON string from Task 1 back into a Python dictionary. Print the student's name, the second marks value, and the city from the nested address.

Task 3 — Identify and Fix Invalid JSON The following JSON string contains two syntax errors. Identify them in a comment, fix the string, parse it using json.loads(), and print the result.\n\npython\nbad_json = '{ name: \"Raj\", \"score\": 88, \"active\": true, }'\n

Task 4 — Build a JSON Array of Objects Create a Python list of three dictionaries, each representing a product with keys product_name, price, and in_stock (boolean). Convert the list to a JSON string with indent=2 and print it.

Submission Guidelines
Use any online Python compiler without AI assistance.
Run your code fully and verify all outputs before submitting.
Select Python as the language from the dropdown at the top of the submission box.
Once verified, paste your complete working code into the submission box.