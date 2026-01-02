from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import easyocr
import cv2
import numpy as np
import pandas as pd
import os
from rapidfuzz import process, fuzz, utils

medicine_db = None
reader = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global medicine_db, reader
    print("🚀 Starting backend...")

    # Load OCR model ONCE at startup
    print("🔄 Loading EasyOCR model (startup warm-up)...")
    reader = easyocr.Reader(
    ['en'],
    gpu=False,
    verbose=False,
    quantize=True  # 👈 this is critical
)

    print("✅ EasyOCR ready")

    if os.path.exists("master_medicines.csv"):
        medicine_db = pd.read_csv("master_medicines.csv")
        medicine_db["search_key"] = (
            medicine_db["name"].astype(str).str.lower().str.strip()
        )
        print("✅ Medicine DB loaded")
    else:
        print("⚠️ Medicine DB not found")

    yield

    reader = None
    medicine_db = None
    print("🛑 Shutdown complete")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresh


def get_cheaper_alternative(name, price):
    if medicine_db is None:
        return None

    matches = medicine_db[
        medicine_db["search_key"].str.contains(name.split()[0].lower(), na=False)
    ]
    cheaper = matches[matches["price"] < price].sort_values("price")

    if cheaper.empty:
        return None

    best = cheaper.iloc[0]
    return {
        "name": best["name"],
        "price": float(best["price"]),
        "manufacturer": best.get("manufacturer", "Unknown"),
        "savings": float(price - best["price"]),
    }


def analyze(image_bytes):
    processed = preprocess_image(image_bytes)
    texts = reader.readtext(processed, detail=0)

    output = []
    for text in texts:
        if len(text) < 4:
            continue

        if medicine_db is not None:
            match = process.extractOne(
                utils.default_process(text),
                medicine_db["search_key"],
                scorer=fuzz.WRatio,
            )
            if match and match[1] > 55:
                row = medicine_db.iloc[match[2]]
                price = float(row["price"])
                output.append({
                    "detected_name": row["name"],
                    "price": price,
                    "type": row.get("type", "Generic"),
                    "buy_link": f"https://www.google.com/search?q=buy+{row['name'].replace(' ', '+')}",
                    "alternative": get_cheaper_alternative(row["name"], price),
                })
                continue

        output.append({
            "detected_name": text,
            "price": "N/A",
            "type": "Unknown",
            "buy_link": f"https://www.google.com/search?q=buy+{text.replace(' ', '+')}",
            "alternative": None,
        })

    return output


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    image = await file.read()
    return {"medicines": analyze(image)}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
