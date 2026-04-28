"""
Generate additional unique complaints to reach 150k total
"""

import csv
import random
from datetime import datetime, timedelta
import os

random.seed(42)

ELECTRICITY_KEYWORDS = {
    "high": ["power outage", "no electricity", "blackout", "complete darkness", "voltage fluctuation", 
             "transformer failure", "pole down", "wire Fallen", "electric shock", "fire hazard",
             "dangerous pole", "live wire", "power surge", "electrical fire", "spark explosion",
             "meter exploded", "dangerous transformer", "power line down", "short circuit", "complete failure",
             "power cut emergency", "electric pole dangerous", "high voltage", "danger to life",
             "power line touching tree", "electrical danger", "transformer burnt", "fuse blown",
             "power failure affecting", "no power days", "continuous outages", "repeated power cuts"],
    "low": ["meter reading", "bill correction", "new connection", "name transfer", "load enhancement",
            "voltage problem", "flickering lights", "billing query", "payment issue", "connection shift",
            "power backup", "generator needed", "inverter installation", "solar setup", "tariff inquiry",
            "bill dispute", "duplicate bill", "payment not reflected", "low voltage", "power fluctuation"]
}

WATER_KEYWORDS = {
    "high": ["no water supply", "water shortage", "pipeline burst", "leaking main", "contaminated water",
             "dirty water", "brown water", "smelly water", "health hazard", "drinking water unsafe",
             "no water days", "tanker needed", "severe shortage", "water crisis", "emergency supply",
             " contaminated supply", "disease causing", "medical issue", "hospital water", "no water pump",
             "tank overflow", "flooding", "pipeline broken", "main leak", "water logging"],
    "low": ["water bill", "new connection", "meter installation", "pipeline repair", "leakage minor",
            "pressure low", "supply timing", "tanker request", "bill correction", "name change",
            "connection transfer", "pressure issue", "meter reading", "quality test", "tariff inquiry"]
}

SEWAGE_KEYWORDS = {
    "high": ["drainage blocked", "sewage overflow", "manhole overflow", "garbage piling", "health hazard",
             "sewage backup", "toilet overflow", "drainage choke", "garbage not collected", "overflowing drain",
             "sewage leak", "bad smell", "mosquito breeding", "rodent infestation", "disease risk",
             "garbage heap", "waste accumulation", "choked drain", "sewage stagnating", "overflowing gutter"],
    "low": ["garbage collection", "bin replacement", "collection timing", "drain cleaning", "street cleaning",
            "bin location", "collection missed", "recycling bin", "waste segregation", "awareness needed",
            "cleaning schedule", "drainage cleaning", "bin repair", "collection frequency", "more bins"]
}

LOCATION_MODIFIERS = [
    "in residential area", "in our locality", "in neighborhood", "in apartment complex",
    "in slum area", "in market area", "near school", "near hospital", "near temple",
    "in old city", "near railway station", "in commercial area", "near bus stand",
    "in industrial zone", "near park", "in colony", "in gated community"
]

def generate_complaint(category, severity):
    if category == "Electricity":
        keywords = ELECTRICITY_KEYWORDS
    elif category == "Water Supply":
        keywords = WATER_KEYWORDS
    else:
        keywords = SEWAGE_KEYWORDS
    
    base = random.choice(keywords[severity.lower()])
    location = random.choice(LOCATION_MODIFIERS)
    
    complaint = f"{base}, {location}"
    
    if severity == "High" and random.random() < 0.3:
        complaint += ", urgent attention required"
    
    # Timestamp
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    timestamp = start_date + timedelta(days=random_days, seconds=random.randint(0, 86399))
    
    # Status
    if severity == "High":
        status = random.choice(["Pending", "In Progress", "Resolved"])
    else:
        status = random.choice(["Pending", "Resolved", "Closed"])
    
    return complaint, timestamp.strftime("%Y-%m-%d %H:%M:%S"), status

# Generate 50k new records (CF-150001 to CF-200000)
start_id = 150001
num_records = 50000
categories = ["Electricity", "Water Supply", "Waste-Water/Sewage"]

rows = []
for i in range(num_records):
    if i % 10000 == 0:
        print(f"Generating: {i}/{num_records}")
    
    category = random.choice(categories)
    severity = random.choice(["High", "Low"])
    
    complaint, timestamp, status = generate_complaint(category, severity)
    complaint_id = f"CF-{start_id + i}"
    
    rows.append([complaint_id, complaint, category, severity, timestamp, status])

# Save
output_path = os.path.join(os.path.dirname(__file__), "..", "data", "complaints_150k.csv")
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Complaint_ID', 'Complaint_Text', 'Category', 'Severity', 'Date', 'Status'])
    writer.writerows(rows)

print(f"Saved {num_records} records to {output_path}")

# Now merge all 4 datasets
import pandas as pd

dfs = []
for path in [
    os.path.join(os.path.dirname(__file__), "..", "data", "complaints_dataset.csv"),
    os.path.join(os.path.dirname(__file__), "..", "data", "complaints_150k.csv")
]:
    df = pd.read_csv(path)
    df.columns = ['Complaint_ID', 'Complaint_Text', 'Category', 'Severity', 'Date', 'Status']
    dfs.append(df)
    print(f"Loaded {len(df)} rows from {os.path.basename(path)}")

combined = pd.concat(dfs, ignore_index=True)
combined = combined.drop_duplicates(subset=['Complaint_ID'], keep='first')
combined = combined.dropna(subset=['Complaint_Text', 'Category', 'Severity'])

# Filter valid categories
combined = combined[combined['Category'].isin(['Electricity', 'Water Supply', 'Waste-Water/Sewage'])]

print(f"\nTotal unique records: {len(combined)}")
print("\nBy Category:")
print(combined['Category'].value_counts())
print("\nBy Severity:")
print(combined['Severity'].value_counts())

# Save final combined
output_path = os.path.join(os.path.dirname(__file__), "..", "data", "complaints_150k_final.csv")
combined.to_csv(output_path, index=False, encoding='utf-8')
print(f"\nSaved 150k dataset to: {output_path}")