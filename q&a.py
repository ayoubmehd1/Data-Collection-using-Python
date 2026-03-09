import requests
from bs4 import BeautifulSoup
import json

url = "https://www.nutrition.gov/expert-q-a"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

qa_list = []

for item in soup.select(".field--item"):
    question = item.find("summary", class_="nal-details__title")
    answer = item.find("div", class_="nal-details__content")

    if question and answer:
        qa_list.append({
            "question": question.get_text(strip=True),
            "answer": answer.get_text(strip=True),
            "source": "Nutrition.gov",
            "language": "en"
        })

with open("nutrition_qa.json", "w", encoding="utf-8") as f:
    json.dump(qa_list, f, indent=4, ensure_ascii=False)

print(f"✅ {len(qa_list)} Q&A collected")

import json
import pandas as pd

df = pd.read_parquet("hf://datasets/heliosbrahma/mental_health_chatbot_dataset/data/train-00000-of-00001-01391a60ef5c00d9.parquet")

coaching = []

for _, row in df.iterrows():
     text = str(row["text"]).strip()
     parts = text.split("\n", 1)
     user_msg = parts[0].replace("User:", "").strip()
     assistant_msg = parts[1].replace("Assistant:", "").strip()
     coaching.append({
            "dialogue": [
                {"role": "user", "text": user_msg},
                {"role": "coach", "text": assistant_msg}
            ],
            "type": "coaching",
            "topic": "lifestyle_health",
            "language": "en",
            "source": "heliosbrahma/mental_health_chatbot_dataset"
        })

with open("coaching_examples.json", "w", encoding="utf-8") as f:
    json.dump(coaching, f, indent=4, ensure_ascii=False)

print(f"✅ {len(coaching)} coaching examples extracted")

df = pd.read_json("hf://datasets/Amod/mental_health_counseling_conversations/combined_dataset.json", lines=True)
final_data = []

for _, row in df.iterrows():
    text = str(row.get("text", "")).strip()

    if "User:" in text and "Assistant:" in text:
        context = text.split("User:")[1].split("Assistant:")[0].strip()
        response = text.split("Assistant:")[1].strip()
        final_data.append({
            "dialogue": [
                {"role": "user", "text": context},
                {"role": "counselor", "text": response}
            ],
            "type": "counseling",
            "topic": "mental_health",
            "language": "en",
            "source": "Amod/mental_health_counseling_conversations"
        })
with open("combined_dataset.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"✅ {len(final_data)} records exported")