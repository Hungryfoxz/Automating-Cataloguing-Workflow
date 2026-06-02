from fastapi import FastAPI, UploadFile, File
from typing import List
import shutil
import os
import requests
import base64
import json
import re

app = FastAPI()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

latest_data = {}

MODEL_NAME = "qwen_qwen3.5-0.8b"


# -----------------------------
# 🔧 Extract JSON safely
# -----------------------------

def extract_json(text):
    pass
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    return {"title": ""}


# -----------------------------
# 🤖 Call Vision Model
# -----------------------------
def call_llm_with_image(image_path):
    print("📸 Inside LLM function")

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        prompt = """
                Extract ONLY the book title.

                Return ONLY JSON:
                {"title": "..."}
                """

        response = requests.post(
            "http://localhost:1234/v1/chat/completions",  # LM Studio endpoint
            headers={"Content-Type": "application/json"},
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "temperature": 0.2
            }
        )

        res_json = response.json()
        print("FULL API RESPONSE:", res_json)

        # 🔹 Extract content safely
        content = res_json["choices"][0]["message"]["content"]

        print("MODEL TEXT OUTPUT:", content)

        return extract_json(content)

    except Exception as e:
        print("❌ ERROR:", e)
        return {"title": ""}

# -----------------------------
# 📥 Extract Endpoint
# -----------------------------
@app.post("/extract")
async def extract(images: List[UploadFile] = File(...)):
    global latest_data

    results = []

    for img in images:
        path = os.path.join(UPLOAD_DIR, img.filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

        data = call_llm_with_image(path)
        results.append(data)

    # 🔹 Take first valid title
    final = {"title": ""}

    for r in results:
        if r.get("title"):
            final["title"] = r["title"]
            break
    latest_data = final

    return final


# -----------------------------
# 📤 Latest Endpoint
# -----------------------------
@app.get("/latest")
def get_latest():
    return latest_data