"""
Data Generation Engine for Civic Complaints
Generates 50,000 unique, high-quality complaint records
"""

import csv
import random
import sys
from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import os

# Expanded vocabulary for natural language generation

ELECTRICITY_KEYWORDS = {
    "high": ["power outage", "no electricity", "blackout", "complete darkness", "voltage fluctuation", 
             "transformer failure", "pole down", "wire fallen", "electric shock", "fire hazard",
             "dangerous pole", "live wire", "power surge", "electrical fire", "spark explosion",
             "meter exploded", "dangerous transformer", "power line down", "短路", "complete failure",
             "power cut emergency", "electric pole dangerous", "high voltage", "danger to life",
             "power line touching tree", "electrical danger", "transformer burnt", "fuse blown",
             "power failure affecting", "no power days", "continuous outages", "repeated power cuts",
             "frequent failures", "hour-long outage", "severe voltage drop", "zero power"],
    "low": ["meter reading", "bill correction", "new connection", "name transfer", "load enhancement",
            "voltage problem", "flickering lights", "billing query", "payment issue", "connection shift",
            "power backup", "generator needed", "inverter installation", "solar setup", "tariff inquiry",
            "bill dispute", "duplicate bill", "payment not reflected", "low voltage", "power fluctuation",
            "uneven supply", "intermittent power", "occasional cut", "momentary outage",
            "light issue", "billing clarification", "subsidy needed", "rebate inquiry",
            "connection status", "meter testing", "bill amount", "payment mode", "online payment"]
}

WATER_KEYWORDS = {
    "high": ["no water supply", "water shortage", "pipeline burst", "leaking main", "contaminated water",
             "dirty water", "brown water", "smelly water", "health hazard", "drinking water unsafe",
             "no water days", "tanker needed", "severe shortage", "water crisis", "emergency supply",
             " contaminated supply", "disease causing", "medical issue", "hospital water", "no water pump",
             "tank overflow", "flooding", "pipeline broken", "main leak", "water logging",
             "contaminated well", "chemical smell", "rusty water", "greenish water", "waterborne disease",
             "diarrhea cases", "children sick", "elderly suffering", "no water for cooking", "critical shortage"],
    "low": ["water bill", "new connection", "meter installation", "pipeline repair", "leakage minor",
            "pressure low", "supply timing", "tanker request", "bill correction", "name change",
            "connection transfer", "pressure issue", "meter reading", "quality test", "tariff inquiry",
            "billing query", "minor leakage", "supply schedule", "water timing", "tank cleaning",
            "filter needed", "pressure problem", "supply delay", "timing change", "bill dispute",
            "connection fee", "deposit refund", "meter shift", "pipeline shift", "supply query"]
}

SEWAGE_KEYWORDS = {
    "high": ["drainage blocked", "sewage overflow", "manhole overflow", "garbage piling", "health hazard",
             "sewage backup", "toilet overflow", "drainage choke", "garbage not collected", "overflowing drain",
             "sewage leak", "bad smell", "mosquito breeding", "rodent infestation", "disease risk",
             "garbage heap", "waste accumulation", "choked drain", "sewage stagnating", "overflowing gutter",
             "garbage crisis", "waste dumped", "illegal dumping", "overflowing bin", "sewage spill",
             "drainage failure", "sewage contamination", "garbage outbreak", "drainage backup", "waste smell",
             "blockage severe", "garbage everywhere", "sewage on road", "public health", "cleanliness emergency"],
    "low": ["garbage collection", "bin replacement", "collection timing", "drain cleaning", "street cleaning",
            "bin location", "collection missed", "recycling bin", "waste segregation", "awareness needed",
            "cleaning schedule", "drainage cleaning", "bin repair", "collection frequency", "more bins",
            "separate bins", "composting", "recycling pickup", "bulk waste", "construction debris",
            "drain slow", "minor blockage", "cleaning request", "drainage maintenance", "dustbin needed",
            "garbage truck", "sanitation worker", "cleaning service", "waste management", "drainage query"]
}

LOCATION_MODIFIERS = [
    "in residential area", "in our locality", "in the neighborhood", "in apartment complex",
    "in slum area", "in market area", "near school", "near hospital", "near temple",
    "in old city", "near railway station", "in commercial area", "near bus stand",
    "in industrial zone", "near park", "in colony", "in gated community",
    "near playground", "in crowded area", "near hospital"
]

URGENCY_PHRASES = [
    "urgent attention required", "immediate action needed", "serious issue", "please resolve ASAP",
    "critical situation", "emergency", "hazardous condition", "dangerous", "life threatening",
    "affecting children", "elderly at risk", "medical emergency", "safety concern",
    "cannot wait", "needs quick action", "waiting for resolution"
]

CONTEXT_PHRASES = [
    "since yesterday", "for past 3 days", "since morning", "last week",
    "for several days", "since past week", "continuous problem",
    "recurring issue", "repeated failure", "frequent occurrence",
    "every day", "multiple times", "regular problem", "ongoing issue",
    "past month", "recently", "last night", "this morning"
]

AFFECTED_PHRASES = [
    "affecting 50 families", "hundreds affected", "entire street suffering",
    "whole area affected", "many residents troubled", "multiple families",
    "whole neighborhood", "entire locality", "affecting residents",
    "hundreds facing", "multiple households", "community affected",
    "over 100 families", "dozens受影响", "many people suffering"
]

PROBLEM_CONTEXT = [
    "causing inconvenience", "difficult situation", "troubled residents",
    "facing difficulties", "severe problem", "major hassle",
    "daily struggle", "serious trouble", "problem for residents",
    "hardship for people", "affecting daily life", "creating trouble"
]

def generate_natural_complaint(category: str, severity: str, existing_ids: set) -> Tuple:
    """Generate a natural-sounding complaint with proper classification."""
    
    if category == "Electricity":
        keywords = ELECTRICITY_KEYWORDS
        category_prefixes = ["Power failure", "Electricity", "Voltage", "Electrical", "Power supply", "Electric"]
    elif category == "Water Supply":
        keywords = WATER_KEYWORDS
        category_prefixes = ["Water supply", "Drinking water", "Pipeline", "Water main", "Tap water", "Water connection"]
    else:
        keywords = SEWAGE_KEYWORDS
        category_prefixes = ["Drainage", "Sewage", "Garbage", "Waste water", "Drainage system", "Sanitation"]
    
    # Choose base problem description based on severity
    if severity == "High":
        base_problems = keywords["high"]
        use_urgency = random.random() < 0.5
        use_context = random.random() < 0.7
        use_affected = random.random() < 0.4
    else:
        base_problems = keywords["low"]
        use_urgency = False
        use_context = random.random() < 0.3
        use_affected = False
    
    # Generate base complaint
    base = random.choice(base_problems)
    
    # Vary the complaint structure
    structure = random.randint(1, 4)
    
    if structure == 1:
        complaint = base.capitalize()
    elif structure == 2:
        complaint = f"{base}, {random.choice(CONTEXT_PHRASES)}"
    elif structure == 3:
        complaint = f"{base}, {random.choice(LOCATION_MODIFIERS)}"
    else:
        parts = [base]
        if use_context:
            parts.append(random.choice(CONTEXT_PHRASES))
        if use_affected and severity == "High":
            parts.append(random.choice(AFFECTED_PHRASES))
        if use_urgency and severity == "High":
            parts.append(random.choice(URGENCY_PHRASES))
        complaint = ", ".join(parts)
    
    complaint = complaint.capitalize()
    
    # Assign proper severity based on keywords if not already set
    if severity == "High" or severity == "Low":
        final_severity = severity
    else:
        # Re-check based on content
        urgency_words = ["urgent", "immediately", "emergency", "critical", "dangerous", "serious", "hazard", "life", "children", "hospital"]
        if any(word in complaint.lower() for word in urgency_words):
            final_severity = "High"
        else:
            final_severity = "Low"
    
    # Assign timestamp
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86399)
    timestamp = start_date + timedelta(days=random_days, seconds=random_seconds)
    
    # Assign status based on severity
    if final_severity == "High":
        status = random.choices(["Pending", "In Progress", "Resolved", "Closed"], weights=[45, 30, 20, 5])[0]
    else:
        status = random.choices(["Pending", "In Progress", "Resolved", "Closed"], weights=[20, 20, 40, 20])[0]
    
    return (complaint, category, final_severity, timestamp.strftime("%Y-%m-%d %H:%M:%S"), status)

def generate_complaints(n: int, start_id: int) -> List[Tuple]:
    """Generate n unique complaint records."""
    
    complaints = []
    categories = ["Electricity", "Water Supply", "Waste-Water/Sewage"]
    
    # Distribution: roughly equal categories with at least 40% High severity
    category_weights = [0.34, 0.33, 0.33]  # Slightly more electricity
    severity_weights = [0.42, 0.58]  # At least 40% High
    
    print(f"Generating {n:,} unique complaints...")
    
    for i in range(n):
        if i % 10000 == 0:
            print(f"  Progress: {i:,}/{n:,}")
        
        # Select category and severity based on weights
        category = random.choices(categories, weights=category_weights)[0]
        severity = random.choices(["High", "Low"], weights=severity_weights)[0]
        
        # Generate complaint until unique
        complaint_text, final_category, final_severity, timestamp, status = generate_natural_complaint(category, severity, set())
        
        # Generate unique ID
        complaint_id = f"CF-{start_id + i}"
        
        complaints.append((complaint_id, complaint_text, final_category, final_severity, timestamp, status))
    
    return complaints

def main():
    """Main function to generate and save complaints."""
    
    # Generate 50,000 complaints starting from CF-100001
    start_id = 100001
    num_complaints = 50000
    
    complaints = generate_complaints(num_complaints, start_id)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "complaints_expanded.csv")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Complaint_ID', 'Complaint_Text', 'Category', 'Severity', 'Date', 'Status'])
        writer.writerows(complaints)
    
    # Print statistics
    categories = {"Electricity": 0, "Water Supply": 0, "Waste-Water/Sewage": 0}
    severities = {"High": 0, "Low": 0}
    statuses = {"Pending": 0, "In Progress": 0, "Resolved": 0, "Closed": 0}
    
    for row in complaints:
        categories[row[2]] += 1
        severities[row[3]] += 1
        statuses[row[5]] += 1
    
    print(f"\n=== Generated {num_complaints:,} complaints ===")
    print(f"\nBy Category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count:,} ({count/num_complaints*100:.1f}%)")
    
    print(f"\nBy Severity:")
    for sev, count in severities.items():
        print(f"  {sev}: {count:,} ({count/num_complaints*100:.1f}%)")
    
    print(f"\nBy Status:")
    for stat, count in sorted(statuses.items()):
        print(f"  {stat}: {count:,} ({count/num_complaints*100:.1f}%)")
    
    print(f"\nSaved to: {output_path}")

if __name__ == "__main__":
    main()