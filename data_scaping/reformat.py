import json

# Assuming you have 'phone.json' with the data
with open('phone.json', 'r') as f:
    data = json.load(f)

# Reformat JSON data with indentation (optional)
with open('phone.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)  # Indent for better readability

print("Phone data reformatted in phone.json")
