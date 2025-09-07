"""
Run moderation agent on:
- an internal examples list, OR
- a file data/messages.csv (optional)
Outputs results to reports/moderation_results.csv
"""

import os
import pandas as pd
from agents.moderation_agent import moderate_message

# If you want to test with a CSV, create data/messages.csv with column "message"
csv_path = "data/messages.csv"  # optional

messages = []
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    if "message" in df.columns:
        messages = df["message"].astype(str).tolist()
    else:
        # if CSV doesn't have a "message" column, treat first column as message
        messages = df.iloc[:, 0].astype(str).tolist()
else:
    # fallback examples
    messages = [
        "Call me at 9876543210 for price.",
        "This is a scam, do not buy!",
        "Limited offer, buy now at http://cheap.com",
        "Is this available? interested.",
        "You are stupid and an idiot",
        "Join whatsapp group: +91 98765 43210",
        "LOOOOL!!!!!!!!",
    ]

results = []
for i, msg in enumerate(messages):
    out = moderate_message(msg)
    row = {"message": msg, **out}
    results.append(row)

os.makedirs("reports", exist_ok=True)
pd.DataFrame(results).to_csv("reports/moderation_results.csv", index=False)
print("Saved reports/moderation_results.csv")
print(pd.DataFrame(results).head())
