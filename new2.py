import json

# Read JSON data from file
with open('products/fixtures/categories.json', 'r') as file:
    json_data = json.load(file)

# Function to replace spaces with underscores and convert to lowercase
def process_name(name):
    return name.lower().replace(' ', '_')

# Process each item in the JSON data
for item in json_data:
    fields = item.get('fields', {})  # Get the 'fields' dictionary
    name = fields.get('name', '')  # Get the 'name' value
    fields['name'] = process_name(name)  # Process the 'name' value

# Write the updated JSON data to a new file
with open('categ.json', 'w') as output_file:
    json.dump(json_data, output_file, indent=4)
