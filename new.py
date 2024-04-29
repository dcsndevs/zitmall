import json

# Define the mapping of category names to category values
category_mapping = {
    "AC Bracket": 1,
    "Air Condiitioner": 2,
    "Air Conditioner": 3,
    "Air Conditioners": 4,
    "Air Cooler": 5,
    "Airpod": 6,
    "Apple Ipad": 7,
    "Blender": 8,
    "Ceiling Fan": 9,
    "celling fan": 10,
    "Chest Freezer": 11,
    "CHILLER": 12,
    "Cooker": 13,
    "Cooler": 14,
    "Dispenser": 15,
    "DVD Player": 16,
    "Electric Hotplate": 17,
    "Electric Jug": 18,
    "Extension": 19,
    "Fan": 20,
    "Food Processor": 21,
    "Freezer": 22,
    "Fridge": 23,
    "Gas Cooker": 24,
    "Generator": 25,
    "Home theater": 26,
    "Home Theatre": 27,
    "Hood": 28,
    "Installation Kit": 29,
    "inverter": 30,
    "Inverter Battery": 31,
    "Iphone": 32,
    "Iphone 6S Plus": 33,
    "Iphone Xs": 34,
    "Iphone Xs Max": 35,
    "Iron": 36,
    "Juice Extractor": 37,
    "Kettle": 38,
    "Laptop": 39,
    "Microwave": 40,
    "Microwave Oven": 41,
    "Mobile Phone": 42,
    "Oven": 43,
    "phone": 44,
    "Pressure Cooker": 45,
    "Pressure Pot": 46,
    "Range Hood": 47,
    "Rechargeable Fan": 48,
    "Refrigerator": 49,
    "Regulator": 50,
    "Rice Cooker": 51,
    "smart tv": 52,
    "Smart watch": 53,
    "solar battery": 54,
    "Solar Panel": 55,
    "Sound Bar": 56,
    "Sound Speaker": 57,
    "Sound system": 58,
    "SPEAKER": 59,
    "Stabilizer": 60,
    "Stablizer": 61,
    "Standing Fan": 62,
    "Standing Gas Cooker": 63,
    "Stove": 64,
    "Television": 65,
    "Toaster": 66,
    "TOP MOUNT Refrigerators": 67,
    "Tower Fan": 68,
    "Voltage Protector": 69,
    "Wall Bracket": 70,
    "Wall Fan": 71,
    "Wallpaper TV": 72,
    "Washing Machine": 73,
    "Water Dispenser": 74,
    "Water Heater": 75,
    "Water Kettle": 76,
    "Yam Pounder": 77
}

# Read the existing JSON file
with open('output.json', 'r') as file:
    data = json.load(file)

# Replace category values according to the mapping
for item in data:
    category_name = item['fields']['category']
    item['fields']['category'] = category_mapping.get(category_name, None)

# Write the updated JSON data back to the file
with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)
