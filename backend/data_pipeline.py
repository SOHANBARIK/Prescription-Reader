import pandas as pd
import re
import os

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove special chars, keep alphanumeric + space
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower().strip()

def load_standard_dataset(file_path, source_type):
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: File not found: {file_path}")
        return pd.DataFrame()

    try:
        # Try reading with different encodings (Real datasets often use cp1252)
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='cp1252')

        print(f"   -> Found columns in {source_type}: {list(df.columns)}")
        
        # Standardize Columns based on Source
        if source_type == 'Janaushadhi':
            # Janaushadhi usually has: 'Generic Name', 'Unit Size', 'MRP'
            # We map whatever exists to our standard names
            col_map = {
                'Generic Name': 'name', 'GENERIC NAME': 'name',
                'MRP': 'price', 'Unit Price': 'price',
                'Unit Size': 'pack_size'
            }
            df = df.rename(columns=col_map)
            df['manufacturer'] = 'Janaushadhi (Govt)'
            df['type'] = 'Generic'
            
        elif source_type == 'Kaggle':
            # Kaggle usually has: 'medicine_name', 'manufacturer_name', 'price'
            col_map = {
                'medicine_name': 'name', 'name': 'name',
                'manufacturer_name': 'manufacturer', 'manufacturer': 'manufacturer',
                'price': 'price', 'mrp': 'price'
            }
            df = df.rename(columns=col_map)
            df['type'] = 'Brand'

        # Ensure required columns exist
        required = ['name', 'price', 'manufacturer', 'type']
        for col in required:
            if col not in df.columns:
                print(f"   ❌ Error: Column '{col}' missing in {source_type}. Dropping bad rows.")
                return pd.DataFrame()

        # Convert Price to Numeric (Real data often has strings like "Rs. 50")
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Clean Names
        df.dropna(subset=['name', 'price'], inplace=True)
        df['source'] = source_type
        
        return df[required + ['source']]

    except Exception as e:
        print(f"❌ Critical Error reading {source_type}: {e}")
        return pd.DataFrame()

def merge_datasets(jan_path, kaggle_path, output_path):
    print("🚀 Starting Data Pipeline for REAL Datasets...")
    
    # 1. Load Data
    df_jan = load_standard_dataset(jan_path, 'Janaushadhi')
    print(f"✅ Loaded {len(df_jan)} Generic medicines.")
    
    df_kaggle = load_standard_dataset(kaggle_path, 'Kaggle')
    print(f"✅ Loaded {len(df_kaggle)} Branded medicines.")

    # 2. Merge
    if df_jan.empty and df_kaggle.empty:
        print("❌ Error: No data loaded. Check file names and paths.")
        return

    master_df = pd.concat([df_jan, df_kaggle], ignore_index=True)
    
    # 3. Create Search Key (Critical for Fuzzy Match)
    print("⚙️  Generating Search Keys (This may take a moment)...")
    master_df['search_key'] = master_df['name'].apply(clean_text)
    
    # 4. Save
    master_df.to_csv(output_path, index=False)
    print(f"🎉 Success! Master Database saved to: {output_path}")
    print(f"📊 Total Medicines: {len(master_df)}")

if __name__ == "__main__":
    # Ensure we look in the current directory or 'backend'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    merge_datasets(
        os.path.join(base_dir, 'janaushadhi_data.csv'),
        os.path.join(base_dir, 'indian_medicines.csv'),
        os.path.join(base_dir, 'master_medicines.csv')
    )