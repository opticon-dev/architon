path = r"C:\Users\이정현\Documents\architon\task1_data\input\material_for_project.csv"
json_path = r"C:\Users\이정현\Documents\architon\task1_data\input\material.json"

import pandas as pd
import json

df = pd.read_csv(path)
print(df)

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)


def get_material_price(material_name, material_list):
    for material in material_list:
        if material["name"] == material_name:
            return float(material["price"])
    raise ValueError("material not found")


total_price = 0
for i, row in df.iterrows():
    material = row["name"]
    price = get_material_price(material, data)
    count = float(row["count"])

    total_price += price * count

print(f"총 가격 : {total_price}")
