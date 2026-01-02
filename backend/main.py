from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
import cv2
import numpy as np
import pandas as pd
from rapidfuzz import process, fuzz, utils
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

medicine_db = pd.read_csv("master_medicines.csv")
medicine_db["search_key"] = medicine_db["name"].str.lower().str.strip()


def preprocess(image_bytes):
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    return cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def extract_text(image):
    return pytesseract.image_to_string(image)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    image_bytes = await file.read()
    processed = preprocess(image_bytes)
    text = extract_text(processed)

    results = []
    for line in text.split("\n"):
        line = line.strip()
        if len(line) < 4:
            continue

        match = process.extractOne(
            utils.default_process(line),
            medicine_db["search_key"],
            scorer=fuzz.WRatio,
        )

        if match and match[1] > 55:
            row = medicine_db.iloc[match[2]]
            results.append({
                "detected_name": row["name"],
                "price": float(row["price"]),
                "type": row.get("type", "Generic"),
            })

    return {"medicines": results}


@app.get("/healthz")
def health():
    return {"status": "ok"}
