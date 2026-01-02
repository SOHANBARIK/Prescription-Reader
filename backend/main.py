from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import io
import cv2
import numpy as np
from rapidfuzz import process, fuzz, utils
import pandas as pd
from contextlib import asynccontextmanager
import os

# --- Global Variables ---
medicine_db = None
reader = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global medicine_db, reader
    print("Loading AI Model...")
    reader = easyocr.Reader(['en'], gpu=False) 
    
    if os.path.exists("master_medicines.csv"):
        medicine_db = pd.read_csv("master_medicines.csv")
        if 'search_key' not in medicine_db.columns:
            medicine_db['search_key'] = medicine_db['name'].astype(str).apply(lambda x: x.lower().strip())
        print("✅ Medicine Database Loaded!")
    else:
        print("⚠️ Warning: master_medicines.csv not found.")
    yield
    medicine_db = None
    reader = None

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_cheaper_alternative(medicine_name, current_price):
    if medicine_db is None: return None
    search_term = medicine_name.split()[0].lower()
    matches = medicine_db[medicine_db['search_key'].str.contains(search_term, na=False)]
    cheaper_options = matches[matches['price'] < current_price].sort_values(by='price')
    
    if not cheaper_options.empty:
        best = cheaper_options.iloc[0]
        return {"name": best['name'], "price": float(best['price']), "manufacturer": best['manufacturer'], "savings": float(current_price - best['price'])}
    return None

def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def analyze_and_recommend(image_bytes):
    processed_img = preprocess_image(image_bytes)
    results = reader.readtext(processed_img, detail=0)
    
    output_data = []
    # Added "syp" (Syrup) to keywords since your image has it
    keywords = ['tab', 'cap', 'syp', 'syrup', 'mg', 'ml', 'tablet', 'capsule']
    potential_meds = [line for line in results if any(k in line.lower() for k in keywords)]
    if not potential_meds: potential_meds = results

    for raw_text in potential_meds:
        if len(raw_text) < 4: continue
        
        if medicine_db is not None:
            match = process.extractOne(utils.default_process(raw_text), medicine_db['search_key'], scorer=fuzz.WRatio)
            if match and match[1] > 55: # Lowered threshold slightly for handwriting
                matched_row = medicine_db.iloc[match[2]]
                price = float(matched_row['price'])
                output_data.append({
                    "detected_name": matched_row['name'],
                    "original_text": raw_text,
                    "price": price,
                    "type": matched_row['type'],
                    "buy_link": f"https://www.google.com/search?q=buy+{matched_row['name'].replace(' ', '+')}",
                    "alternative": get_cheaper_alternative(matched_row['name'], price)
                })
                continue
        
        output_data.append({
            "detected_name": raw_text,
            "original_text": raw_text,
            "price": "N/A",
            "type": "Unknown",
            "buy_link": f"https://www.google.com/search?q=buy+{raw_text.replace(' ', '+')}",
            "alternative": None
        })
    return output_data

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"medicines": analyze_and_recommend(content)}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Medicine OCR and Recommendation API is running."}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)