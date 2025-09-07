import sys
import re
import json
from pathlib import Path
import pandas as pd
import numpy as np

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows from {path}")
    return df

def normalize_condition(val):
    if pd.isna(val):
        return np.nan
    v = str(val).strip().lower()
    if "like" in v:
        return "Like New"
    if v.startswith("good"):
        return "Good"
    if "fair" in v:
        return "Fair"
    return val.title()

def parse_price(val):
    if pd.isna(val):
        return np.nan
    s = re.sub(r"[^\d\.]", "", str(val))
    try:
        return float(s) if s != "" else np.nan
    except:
        return np.nan

def parse_age(val):
    if pd.isna(val):
        return np.nan
    try:
        return int(float(val))
    except:
        m = re.search(r"(\d+)", str(val))
        return int(m.group(1)) if m else np.nan

def category_normalize(cat):
    if pd.isna(cat):
        return "Other"
    c = str(cat).strip().lower()
    mapping = {
        "mobile": "Mobile",
        "laptop": "Laptop",
        "furniture": "Furniture",
        "electronics": "Electronics",
        "camera": "Camera",
        "fashion": "Fashion",
    }
    return mapping.get(c, cat.title())

def remove_price_outliers(df, col="asking_price"):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
    return df[(df[col] >= low) & (df[col] <= high)].reset_index(drop=True)

def main(in_path, out_path):
    df = load_csv(in_path)
    df["asking_price"] = df["asking_price"].apply(parse_price)
    df["age_months"] = df["age_months"].apply(parse_age)
    df["condition"] = df["condition"].apply(normalize_condition)
    df["category"] = df["category"].apply(category_normalize)

    # Handle missing values
    df["asking_price"] = df["asking_price"].fillna(df["asking_price"].median())
    df["age_months"] = df["age_months"].fillna(df["age_months"].median())

    # Remove outliers
    df = remove_price_outliers(df, "asking_price")

    # Save outputs
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved cleaned dataset → {out_path}")

    profile = {
        "rows": len(df),
        "median_price_by_category": df.groupby("category")["asking_price"].median().to_dict(),
    }
    with open("reports/data_profile.json", "w") as f:
        json.dump(profile, f, indent=2)
    print("Saved profile → reports/data_profile.json")

if __name__ == "__main__":
    main("data/products.csv", "data/cleaned_products.csv")
import sys
import re
import json
from pathlib import Path
import pandas as pd
import numpy as np

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows from {path}")
    return df

def normalize_condition(val):
    if pd.isna(val):
        return np.nan
    v = str(val).strip().lower()
    if "like" in v:
        return "Like New"
    if v.startswith("good"):
        return "Good"
    if "fair" in v:
        return "Fair"
    return val.title()

def parse_price(val):
    if pd.isna(val):
        return np.nan
    s = re.sub(r"[^\d\.]", "", str(val))
    try:
        return float(s) if s != "" else np.nan
    except:
        return np.nan

def parse_age(val):
    if pd.isna(val):
        return np.nan
    try:
        return int(float(val))
    except:
        m = re.search(r"(\d+)", str(val))
        return int(m.group(1)) if m else np.nan

def category_normalize(cat):
    if pd.isna(cat):
        return "Other"
    c = str(cat).strip().lower()
    mapping = {
        "mobile": "Mobile",
        "laptop": "Laptop",
        "furniture": "Furniture",
        "electronics": "Electronics",
        "camera": "Camera",
        "fashion": "Fashion",
    }
    return mapping.get(c, cat.title())

def remove_price_outliers(df, col="asking_price"):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
    return df[(df[col] >= low) & (df[col] <= high)].reset_index(drop=True)

def main(in_path, out_path):
    df = load_csv(in_path)
    df["asking_price"] = df["asking_price"].apply(parse_price)
    df["age_months"] = df["age_months"].apply(parse_age)
    df["condition"] = df["condition"].apply(normalize_condition)
    df["category"] = df["category"].apply(category_normalize)

    # Handle missing values
    df["asking_price"] = df["asking_price"].fillna(df["asking_price"].median())
    df["age_months"] = df["age_months"].fillna(df["age_months"].median())

    # Remove outliers
    df = remove_price_outliers(df, "asking_price")

    # Save outputs
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved cleaned dataset → {out_path}")

    profile = {
        "rows": len(df),
        "median_price_by_category": df.groupby("category")["asking_price"].median().to_dict(),
    }
    with open("reports/data_profile.json", "w") as f:
        json.dump(profile, f, indent=2)
    print("Saved profile → reports/data_profile.json")

if __name__ == "__main__":
    main("data/products.csv", "data/cleaned_products.csv")
