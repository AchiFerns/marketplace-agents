# src/save_report.py
import csv, os
from datetime import datetime

OUT = "reports/price_suggestions.csv"
os.makedirs("reports", exist_ok=True)

def save_suggestion(product, result):
    header = ["time","title","brand","age_months","asking_price","min","max","reason","llm_provider","llm_model"]
    row = [
        datetime.utcnow().isoformat(),
        product.get("title",""),
        product.get("brand",""),
        product.get("age_months",""),
        product.get("asking_price",""),
        result.get("suggested_price_min",""),
        result.get("suggested_price_max",""),
        result.get("reason","").replace("\n"," "),
        result.get("llm_provider",""),
        result.get("llm_model",""),
    ]
    write_header = not os.path.exists(OUT)
    with open(OUT,"a",newline="",encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(header)
        w.writerow(row)
