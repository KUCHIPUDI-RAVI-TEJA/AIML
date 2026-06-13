import json
# task1
task1 = {
    "name": "Ravi Teja",
    "age": 22,
    "passed": True,
    "marks": [90, 89, 91],
    "address": {
        "city": "Hyderabad",
        "pincode": 534340
    }
}

json_string = json.dumps(task1, indent=4)
print(json_string)

# Task2
json_load = json.loads(json_string)
print(json_load.get("name"))
print(json_load.get("marks"))
print(json_load.get("address").get("city"))

#TASk 3

#\n\npython\nbad_json = '{ name: \"Raj\", \"score\": 88, \"active\": true, }'\n
#name not enclosed in double quotes
# trailing comma at the end
good_json = '{ "name": \"Raj\", \"score\": 88, \"active\": true }'
print(json.loads(good_json))

#Task4
json_arr = [
    {
        "product_name":"Product 1",
        "price":2000,
        "in_stock":True
    },
    {
        "product_name":"Product 2",
        "price":2000,
        "in_stock":True
    },
    {
        "product_name":"Product 3",
        "price":2000,
        "in_stock":False
    },
]

print(json.dumps(json_arr, indent=2))