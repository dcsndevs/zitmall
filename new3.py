# Subcategories data
subcategories = [
    "Air Conditioner",
    "Airpod",
    "Apple Ipad",
    "DVD Player",
    "Electric Hotplate",
    "Electric Jug",
    "Generator",
    "Home Theater",
    "Home Theatre",
    "Iphone",
    "Iphone 6S Plus",
    "Iphone Xs",
    "Iphone Xs Max",
    "Laptop",
    "Mobile Phone",
    "Smart TV",
    "Smart Watch",
    "Solar Panel",
    "Sound Bar",
    "Sound Speaker",
    "Sound System",
    "Television",
    "Blender",
    "Cooker",
    "Food Processor",
    "Kettle",
    "Microwave",
    "Microwave Oven",
    "Oven",
    "Pressure Cooker",
    "Rice Cooker",
    "Toaster",
    "Yam Pounder",
    "Air Cooler",
    "Chest Freezer",
    "Cooler",
    "Dispenser",
    "Fan",
    "Freezer",
    "Fridge",
    "Gas Cooker",
    "Refrigerator",
    "Rechargeable Fan",
    "Stove",
    "Tower Fan",
    "TOP MOUNT Refrigerators",
    "Washing Machine",
    "Water Dispenser",
    "Water Heater",
    "Water Kettle",
    "Ceiling Fan",
    "Electric Fan",
    "Standing Fan",
    "Wall Fan",
    "Extension",
    "Inverter",
    "Inverter Battery",
    "Iron",
    "Regulator",
    "Stabilizer",
    "Voltage Protector",
    "Entertainment",
    "DVD Player",
    "Home Theater",
    "Home Theatre",
    "Smart TV",
    "Sound Bar",
    "Sound Speaker",
    "Sound System",
    "Television",
    "Gadgets",
    "Airpod",
    "Apple Ipad",
    "Iphone",
    "Iphone 6S Plus",
    "Iphone Xs",
    "Iphone Xs Max",
    "Laptop",
    "Mobile Phone",
    "Smart Watch",
    "Kitchen Essentials",
    "Blender",
    "Cooker",
    "Food Processor",
    "Kettle",
    "Microwave",
    "Microwave Oven",
    "Oven",
    "Pressure Cooker",
    "Rice Cooker",
    "Toaster",
    "Yam Pounder",
    "Home Comfort",
    "Air Cooler",
    "Ceiling Fan",
    "Electric Fan",
    "Tower Fan",
    "Rechargeable Fan",
    "Standing Fan",
    "Wall Fan",
    "Home Improvement",
    "Air Conditioner",
    "Generator",
    "Installation Kit",
    "Solar Panel",
    "Wallpaper TV"
]

# Generate links for subcategories
links = []
for subcategory in subcategories:
    # Convert subcategory to lowercase and replace spaces with underscores
    subcategory_link = subcategory.lower().replace(" ", "_")
    # Create link HTML
    link_html = f'<a class="dropdown-item" href="{{% url \'products\' %}}?category={subcategory_link}">{subcategory}</a>'
    # Append to links list
    links.append(link_html)

# Write links to a text file
with open("subcategories_links.txt", "w") as f:
    for link in links:
        f.write(link + "\n")