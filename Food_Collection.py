import requests
import json
import pandas as pd
import re

url = "https://world.openfoodfacts.org/cgi/search.pl"
product_name = "nugget"

foods = []
MAX_PRODUCTS = 2000
PAGE_SIZE = 200
page = 1

while len(foods) < MAX_PRODUCTS:

    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": PAGE_SIZE,
        "page": page,
        "lc": "en"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "products" not in data or len(data["products"]) == 0:
        print("❌ No more products found.")
        break

    for product in data["products"]:

        if len(foods) >= MAX_PRODUCTS:
            break

        # 🔹 Extraire serving size en grammes
        serving_text = product.get("serving_size", "")
        serving_g = None
        if serving_text:
            match = re.search(r"(\d+)\s*g", serving_text)
            if match:
                serving_g = int(match.group(1))

        # 🔹 Ingrédients en liste
        ingredients_text = product.get("ingredients_text_en") or product.get("ingredients_text") or ""
        if ingredients_text in ["", "undefined", "null", "none"]:
            continue
        ingredients_list = [i.strip() for i in ingredients_text.split(",") if i.strip()]
        
        food = {
            "id": "",

            "name": product.get("product_name_en") or product.get("product_name", ""),
            "image": product.get("image_url", ""),

            "calories_kcal": product.get("nutriments", {}).get("energy-kcal_100g", 0),
            "protein_g": product.get("nutriments", {}).get("proteins_100g", 0),
            "fat_g": product.get("nutriments", {}).get("fat_100g", 0),
            "sugars_g": product.get("nutriments", {}).get("sugars_100g", 0),

            # ✅ ajouté
            "saturated_fat_g": product.get("nutriments", {}).get("saturated-fat_100g", None),

            "carbs_g": product.get("nutriments", {}).get("carbohydrates_100g", 0),
            "fiber_g": product.get("nutriments", {}).get("fiber_100g", 0),
            "sodium_mg": product.get("nutriments", {}).get("sodium_100g", 0) * 1000,

            "serving_size_g": serving_g,
            "ingredients": ingredients_list,

            "allergens": product.get("allergens", ""),
            "source": "OpenFoodFacts"
        }

        foods.append(food)

    print(f"📄 Page {page} collected — total products: {len(foods)}")
    page += 1
df = pd.DataFrame(foods)


for i,food in enumerate(foods):
    food["id"] = i+1 
with open("nuggets.json", "w", encoding="utf-8") as f:
    json.dump(foods, f, indent=4, ensure_ascii=False)   
print("✅ Data saved to nuggets.json")
   

