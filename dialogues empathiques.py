import string
from matplotlib import text
import pandas as pd
import json
from requests import get


df = pd.read_parquet("hf://datasets/heliosbrahma/mental_health_chatbot_dataset/data/train-00000-of-00001-01391a60ef5c00d9.parquet")
print(df.columns)
print(df.head(1))
conversations = []
for _, row in df.iterrows():
     text = str(row["text"]).strip()
     parts = text.split("\n", 1)
     user_msg = parts[0].replace("User:", "").strip()
     assistant_msg = parts[1].replace("Assistant:", "").strip()
     conversations.append({
        "dialogue": [
            {"role": "user", "text": user_msg},
            {"role": "assistant", "text": assistant_msg}
        ],
        "language": "en",
        "topic": "mental_health_support",
        "source": "heliosbrahma/mental_health_chatbot_dataset"
    })

with open("dialogues empathiques.json", "w", encoding="utf-8") as f:
        json.dump(conversations, f, indent=4, ensure_ascii=False)
print(f"✅ Total conversations collected: {len(conversations)}")