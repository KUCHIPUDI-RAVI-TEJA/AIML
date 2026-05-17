import json

user = {
    "name": "Alice",
    "age": 28,
    "is_active": True
}

json_string = json.dumps(user)
print(json_string)
# Output: {"name": "Alice", "age": 28, "is_active": true}

user = json.loads(json_string)
print(user)
print(user["name"])

response = {
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ]
}

# Get Bob's name
print(response["users"][1]["name"])  # Bob

print(json.dumps(user, indent=4))

# city = user["city"] #KeyError: 'city'
city = user.get("city", "Unknown")

'''
Key Takeaways
JSON is structured text using key-value pairs, wrapped in { }. It's the standard format for sending data between systems, especially APIs.
json.dumps() converts a Python dictionary → JSON string. json.loads() converts a JSON string → Python dictionary.
Always parse first. Call json.loads() on an API response before trying to access any values.
Nested JSON is just JSON inside JSON. Chain your keys (data["a"]["b"]["c"]) to dig into it — and use indexes ([0], [1]) to pull from lists.
Use .get() instead of [] when you're not sure a key will exist — it prevents crashes.
'''
