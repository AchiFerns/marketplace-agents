import pandas as pd
from agents.price_agent import suggest_price

# Load cleaned dataset
df = pd.read_csv("data/cleaned_products.csv")

results = []
for _, row in df.iterrows():
    product = row.to_dict()
    suggestion = suggest_price(product)
    result = {**product, **suggestion}
    results.append(result)

# Save results
out_df = pd.DataFrame(results)
out_df.to_csv("reports/price_suggestions.csv", index=False)
print("✅ Saved price suggestions to reports/price_suggestions.csv")

# Print first 5 rows as preview
print(out_df.head())
