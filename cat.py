import json

data = [
    "AC Bracket",
    "Air Condiitioner",
    "Air Conditioner",
    "Air Conditioners",
    "Air Cooler",
    "Airpod",
    "Apple Ipad",
    "Blender",
    "Ceiling Fan",
    "celling fan",
    "Chest Freezer",
    "CHILLER",
    "Cooker",
    "Cooler",
    "Dispenser",
    "DVD Player",
    "Electric Hotplate",
    "Electric Jug",
    "Extension",
    "Fan",
    "Food Processor",
    "Freezer",
    "Fridge",
    "Gas Cooker",
    "Generator",
    "Home theater",
    "Home Theatre",
    "Hood",
    "Installation Kit",
    "inverter",
    "Inverter Battery",
    "Iphone",
    "Iphone 6S Plus",
    "Iphone Xs",
    "Iphone Xs Max",
    "Iron",
    "Juice Extractor",
    "Kettle",
    "Laptop",
    "Microwave",
    "Microwave Oven",
    "Mobile Phone",
    "Oven",
    "phone",
    "Pressure Cooker",
    "Pressure Pot",
    "Range Hood",
    "Rechargeable Fan",
    "Refrigerator",
    "Regulator",
    "Rice Cooker",
    "smart tv",
    "Smart watch",
    "solar battery",
    "Solar Panel",
    "Sound Bar",
    "Sound Speaker",
    "Sound system",
    "SPEAKER",
    "Stabilizer",
    "Stablizer",
    "Standing Fan",
    "Standing Gas Cooker",
    "Stove",
    "Television",
    "Toaster",
    "TOP MOUNT Refrigerators",
    "Tower Fan",
    "Voltage Protector",
    "Wall Bracket",
    "Wall Fan",
    "Wallpaper TV",
    "Washing Machine",
    "Water Dispenser",
    "Water Heater",
    "Water Kettle",
    "Yam Pounder"
]

# Create JSON structure
json_data = []
for index, category in enumerate(data, start=1):
    entry = {
        "pk": index,
        "model": "products.category",
        "fields": {
            "name": category,
            "friendly_name": category.title()  # Assuming the friendly name is the same as the category name capitalized
        }
    }
    json_data.append(entry)

# Output JSON data to a file
with open('categories.json', 'w') as f:
    json.dump(json_data, f, indent=4)