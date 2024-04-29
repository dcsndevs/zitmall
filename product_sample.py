import json
import pandas as pd

# Read Excel file into a DataFrame
df = pd.read_excel('p5.products.ex.xlsx')

# Convert DataFrame to list of dictionaries
records = df.to_dict(orient='records')

# Create the JSON structure
json_data = []
for index, record in enumerate(records, start=1):
    entry = {
        "pk": index,
        "model": "products.product",
        "fields": record
    }
    json_data.append(entry)

# Write JSON data to a file
with open('output.json', 'w') as f:
    json.dump(json_data, f)
