from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import easyocr
import cv2
import numpy as np
import pandas as pd
import os
from rapidfuzz import process, fuzz, utils

# -----------------------------
# Globals (lazy initialized)
# -----------------------------
medicine_db = None
reader = None


def get_reader():
    """
    Lazy-load EasyOCR reader.
    This prevents Render from OOM-ing during startup.
    """
    global reader
    if reader is None:
        print("🔄 Loading EasyOCR model (lazy)...")
        reader = easyocr.Reader(
            ['en'],
            gpu=False,
            verbose=False
        )
        print("✅ EasyOCR model loaded")
    return reader


@asynccontextmanager
async def lifespan(app: FastAPI):
    global medicine_db
    print("🚀 Starting AushadhiSetu Backend")

    # Load medicine DB if present
    if os.path.exists("master_medicines.csv"):
        medicine_db = pd.read_csv("master_medicines.csv")
        if "search_key" not in medicine_db.columns:
            medicine_db["search_key"] = (
                medicine_db["name"].astype(str).str.lower().str.strip()
            )
        print("✅ Medicine database loaded")
    else:
        print("⚠️ master_medicines.csv not found (running without DB)")

    yield

    print("🛑 Shutting down backend")
    medicine_db = None


app = FastAPI(lifespan=lifespan)

# -----------------------------
# CORS (safe for Vercel)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Helper functions
# -----------------------------
def preprocess_image(image_bytes: bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresh


def get_cheaper_alternative(medicine_name: str, current_price: float):
    if medicine_db is None:
        return None

    search_term = medicine_name.split()[0].lower()
    matches = medicine_db[
        medicine_db["search_key"].str.contains(search_term, na=False)
    ]

    cheaper = matches[matches["price"] < current_price].sort_values("price")

    if cheaper.empty:
        return None

    best = cheaper.iloc[0]
    return {
        "name": best["name"],
        "price": float(best["price"]),
        "manufacturer": best.get("manufacturer", "Unknown"),
        "savings": float(current_price - best["price"]),
    }


def analyze_and_recommend(image_bytes: bytes):
    reader = get_reader()
    processed = preprocess_image(image_bytes)
    results = reader.readtext(processed, detail=0)

    output = []
    keywords = ["tab", "cap", "syp", "syrup", "mg", "ml", "tablet", "capsule"]
    candidates = [
        r for r in results if any(k in r.lower() for k in keywords)
    ] or results

    for text in candidates:
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
                    "original_text": text,
                    "price": price,
                    "type": row.get("type", "Generic"),
                    "buy_link": f"https://www.google.com/search?q=buy+{row['name'].replace(' ', '+')}",
                    "alternative": get_cheaper_alternative(row["name"], price),
                })
                continue

        output.append({
            "detected_name": text,
            "original_text": text,
            "price": "N/A",
            "type": "Unknown",
            "buy_link": f"https://www.google.com/search?q=buy+{text.replace(' ', '+')}",
            "alternative": None,
        })

    return output


# -----------------------------
# Routes
# -----------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    image_bytes = await file.read()
    medicines = analyze_and_recommend(image_bytes)
    return {"medicines": medicines}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "AushadhiSetu OCR API is running"}
