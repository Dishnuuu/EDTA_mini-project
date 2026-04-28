"""
CivicFix - Synthetic Data Generator
Generates 50,000+ realistic government utility complaint records.
Departments: Electricity, Water Supply, Waste-Water/Sewage
Severity: High (safety hazards, outages, flooding) or Low (routine inquiries)
"""

import csv
import random
from datetime import datetime, timedelta
from typing import List, Tuple
import sys


# ============================================================================
# EXPANDED ELECTRICITY COMPLAINTS - HIGH SEVERITY (2000+ unique)
# ============================================================================

ELECTRICITY_HIGH = [
    "Power cut since morning, entire house is dark",
    "Spark coming from electric pole, very dangerous",
    "Electric shock risk near transformer in our area",
    "High voltage wire hanging down on main road, life threatening",
    "Complete blackout in our sector for 12 hours",
    "Transformer exploded, loud noise and fire risk",
    "Electricity pole leaning dangerously, may fall anytime",
    "Live wire exposed near children's play area, emergency",
    "Power surge damaged all appliances, need immediate help",
    "Electrical fire hazard in meter box, smoke coming out",
    "No electricity in hospital area, critical situation",
    "Overloaded transformer making loud buzzing noise, danger",
    "Electric shock from street light pole, someone got hurt",
    "Power lines touching tree branches, fire risk",
    "Complete power failure in entire neighborhood",
    "Electricity board equipment damaged in storm, hazardous",
    "Short circuit causing sparks from main distribution box",
    "Power outage during medical emergency at home",
    "Electrical panel burning smell, evacuation needed",
    "High tension wire broken and lying on road, deadly",
]


def _expand_electricity_high() -> List[str]:
    """Generate expanded high severity electricity complaints."""
    base = [
        "Power cut since morning, entire house is dark",
        "Spark coming from electric pole, very dangerous",
        "Electric shock risk near transformer in our area",
        "High voltage wire hanging down on main road, life threatening",
        "Complete blackout in our sector for 12 hours",
        "Transformer exploded, loud noise and fire risk",
        "Electricity pole leaning dangerously, may fall anytime",
        "Live wire exposed near children's play area, emergency",
        "Power surge damaged all appliances, need immediate help",
        "Electrical fire hazard in meter box, smoke coming out",
    ]
    
    prefixes = ["No electricity", "Power outage", "Load shedding", "Sudden blackout", "Voltage fluctuation",
               "Frequent power cuts", "Erratic electricity", "Unscheduled outage", "Rolling blackouts",
               "Planned maintenance but", "Emergency power cut", "Storm damage causing", "Accident damaged",
               "Transformer failure causing", "Cable fault leading to", "Grid collapse results in",
               "Technical issue causes", "Equipment failure leads to", "Safety protocol triggers"]
    
    suffixes = ["for past 8 hours", "since yesterday", "without notice", "affecting entire block",
               "in residential area", "in our locality", "throughout neighborhood", "across the ward",
               "in market area", "near hospital", "in school zone", "around temple",
               "in old city area", "in apartment complex", "in slum area", "near railway station",
               "in industrial zone", "on main road", "in crowded area", "near water body"]
    
    issues = ["complete power outage", "no electricity supply", "voltage drops to zero", "frequent trippings",
             "no power backup available", "transformer not working", "meter not responding", "power fluctuations damaging appliances",
             "no supply despite payment", "erratic power supply", "intermittent electricity",
             "inconsistent voltage", "low voltage problem", "high voltage spikes",
             "power surging causing damage", "frequent outages", "unscheduled power cuts",
             "prolonged load shedding", "emergency shutdown", "grid failure"]
    
    locations = ["in Sector 12", "near City Hospital", "on MG Road", "in Gandhi Nagar",
               "near Central Park", "in Industrial Area", "near Railway Station",
               "in Old City", "near Shopping Mall", "in Residential Colony",
               "near School Zone", "in Commercial Complex", "near Bus Stand",
               "in VIP Area", "near Market Square", "in Block A", "near Temple",
               "in Housing Board Colony", "near Police Station", "in Slum Area"]
    
    expanded = []
    for p in prefixes:
        for s in suffixes:
            for i in issues:
                for l in locations[:10]:
                    expanded.append(f"{p} {s}, {i} {l}")
                    if len(expanded) >= 1500:
                        break
                if len(expanded) >= 1500:
                    break
            if len(expanded) >= 1500:
                break
        if len(expanded) >= 1500:
            break
    
    return base + expanded[:1500]


def _expand_water_high() -> List[str]:
    """Generate expanded high severity water complaints."""
    base = [
        "No water in tap for 3 days, emergency situation",
        "Pipe burst on main road, water flooding everywhere",
        "Water is muddy and brown, health hazard",
        "Contaminated water supply causing illness in area",
        "Main water pipeline leaked, entire street flooded",
    ]
    
    prefixes = ["No water supply", "Water shortage", "Pipeline burst", "Leak detected", "Contamination",
               "Water logging", "Supply disrupted", "Pipeline damaged", "Contaminated water",
               "Low pressure", "No drinking water", "Water emergency", "Supply failure",
               "Pipeline broken", "Major leak", "Water crisis", "Contamination alert"]
    
    suffixes = ["for past 2 days", "since morning", "without prior notice", "affecting residents",
               "in our area", "throughout locality", "across ward", "in neighborhood",
               "near school", "in hospital zone", "in market", "in temples area",
               "in old city", "in slum", "near railway", "in bus stand"]
    
    issues = ["no water in taps", "severe water shortage", "pipeline burst flooding road",
            "contaminated water supply", "dirty smelly water", "no drinking water",
            "water logging everywhere", "sewage mixed with water", "brown murky water",
            "low water pressure", "no water for days", "supply completely stopped",
            "contaminated well", "chemical smell in water", "rusty water supply",
            "water has bad taste", "particulate matter in water", "fishy odor in water",
            "greenish water", "white particles in water"]
    
    locations = ["in Sector 12", "near City Hospital", "on MG Road", "in Gandhi Nagar",
               "near Central Park", "in Industrial Area", "near Railway Station",
               "in Old City", "near Shopping Mall", "in Residential Colony",
               "near School Zone", "in Commercial Complex", "near Bus Stand",
               "in VIP Area", "near Market Square"]
    
    expanded = []
    for p in prefixes:
        for s in suffixes:
            for i in issues:
                for l in locations[:10]:
                    expanded.append(f"{p} {s}, {i} {l}")
                    if len(expanded) >= 1500:
                        break
                if len(expanded) >= 1500:
                    break
            if len(expanded) >= 1500:
                break
        if len(expanded) >= 1500:
            break
    
    return base + expanded[:1500]


def _expand_sewage_high() -> List[str]:
    """Generate expanded high severity sewage complaints."""
    base = [
        "Drainage blocked, sewage water entering homes",
        "Manhole overflow on main road, traffic hazard",
        "Garbage not collected for 2 weeks, health risk",
        "Sewage water stagnating, mosquito breeding ground",
        "Drainage system completely choked, backflow in toilets",
    ]
    
    prefixes = ["Drainage blocked", "Sewage overflow", "Garbage accumulation", "Manhole issue",
               "Drain blocked", "Sewage backup", "Garbage not collected", "Drainage choked",
               "Sewage leak", "Garbage heap", "Drain overflow", "Manhole overflow",
               "Sewage spill", "Garbage crisis", "Drainage failure", "Sewage blockage"]
    
    suffixes = ["for several days", "since past week", "without collection",
               "causing health hazard", "creating danger", "overflowing repeatedly",
               "in main road", "near residential", "in market area",
               "near school", "in hospital zone", "in temple area",
               "throughout area", "affecting traffic", "near shops"]
    
    issues = ["sewage water entering houses", "manhole covers overflowed",
             "garbage piling everywhere", "drain completely blocked",
             "toilet backflow", "bad smell everywhere", "mosquitoes breeding",
             "rodents appearing", " flies infestation", "disease outbreak risk",
             "children exposed to hazard", "traffic blocked",
             "cannot pass by road", "foul smell unbearable",
             "waste water on road", "garbage scattered everywhere",
             "drainage not working", "sewage stagnation", "waste accumulation"]
    
    locations = ["in Sector 12", "near City Hospital", "on MG Road", "in Gandhi Nagar",
               "near Central Park", "in Industrial Area", "near Railway Station",
               "in Old City", "near Shopping Mall", "in Residential Colony",
               "near School Zone", "in Commercial Complex", "near Bus Stand",
               "in VIP Area", "near Market Square"]
    
    expanded = []
    for p in prefixes:
        for s in suffixes:
            for i in issues:
                for l in locations[:10]:
                    expanded.append(f"{p} {s}, {i} {l}")
                    if len(expanded) >= 1500:
                        break
                if len(expanded) >= 1500:
                    break
            if len(expanded) >= 1500:
                break
        if len(expanded) >= 1500:
            break
    
    return base + expanded[:1500]


def _expand_electricity_low() -> List[str]:
    """Generate expanded low severity electricity complaints."""
    base = ["Meter reading seems incorrect this month", "Need to update name on electricity bill",
           "Request for new electricity connection", "Bill amount higher than usual"]
    
    prefixes = ["Request for", "Need help with", "Want to apply for", "Need information about",
               "Query regarding", "Clarification on", "Want to know about", "Need update on",
               "Application for", "Need to register", "Want to avail", "Request to change"]
    
    suffixes = ["this month", "for my connection", "at earliest", "as soon as possible",
              "in my area", "for our locality", "for new connection", "for shift"]
    
    items = ["name change on electricity bill", "new electricity connection", "bill correction",
            "meter shift", "load enhancement", "tariff information", "payment options",
            "solar connection", "name transfer", "duplicate bill", "new meter installation",
            "load reduction", "connection transfer", "phase upgrade", "voltage stabilization",
            "smart meter", "bill dispute", "rebate application", "subsidy renewal"]
    
    expanded = []
    for p in prefixes:
        for s in suffixes:
            for i in items:
                expanded.append(f"{p} {i} {s}")
                if len(expanded) >= 800:
                    break
        if len(expanded) >= 800:
            break
    
    return base + expanded[:800]


def _expand_water_low() -> List[str]:
    """Generate expanded low severity water complaints."""
    base = ["Water pressure is low in morning hours", "Need to apply for new water connection",
           "Water bill amount seems high", "Request to change name on water bill"]
    
    prefixes = ["Request for", "Need", "Want", "Query about", "Information on",
              "Application for", "Want to apply", "Need clarification"]
    
    items = ["new water connection", "water bill correction", "name change", "meter installation",
            "tariff details", "connection transfer", "pipeline repair", "tanker service",
            "water quality test", "billing query", "connection shift", "borewell permission",
            "pressure improvement", "supply timing change", "rebate", "filter installation"]
    
    locations = ["in my area", "for my house", "at property", "in our locality", "for connection"]
    
    expanded = []
    for p in prefixes:
        for i in items:
            for l in locations:
                expanded.append(f"{p} {i} {l}")
                if len(expanded) >= 800:
                    break
        if len(expanded) >= 800:
            break
    
    return base + expanded[:800]


def _expand_sewage_low() -> List[str]:
    """Generate expanded low severity sewage complaints."""
    base = ["Garbage collection time needs to be earlier", "Request for additional garbage bins",
           "Street cleaning frequency should increase", "Need information about waste segregation"]
    
    prefixes = ["Request for", "Need", "Want", "Query about", "Information on",
              "Want to report", "Need clarification"]
    
    items = ["additional bins", "earlier collection", "more frequent cleaning",
            "recycling service", "segregation guidelines", "composting facility",
            "drain cleaning", "awareness program", "bulk waste removal",
            "bin replacement", "collection schedule change", "separate collection"]
    
    locations = ["in our area", "in my locality", "in market", "near school", "in park"]
    
    expanded = []
    for p in prefixes:
        for i in items:
            for l in locations:
                expanded.append(f"{p} {i} {l}")
                if len(expanded) >= 800:
                    break
        if len(expanded) >= 800:
            break
    
    return base + expanded[:800]


# Generate the expanded lists at module level
ELECTRICITY_HIGH = _expand_electricity_high()
ELECTRICITY_LOW = _expand_electricity_low()
WATER_HIGH = _expand_water_high()
WATER_LOW = _expand_water_low()
WASTE_WATER_HIGH = _expand_sewage_high()
WASTE_WATER_LOW = _expand_sewage_low()

ELECTRICITY_LOW = [
    "Meter reading seems incorrect this month",
    "Need to update name on electricity bill",
    "Request for new electricity connection",
    "Bill amount higher than usual, need clarification",
    "Want to change from prepaid to postpaid meter",
    "Light flickering occasionally in street lamp",
    "Need duplicate copy of electricity bill",
    "Request to shift meter to new location",
    "Power fluctuation issue, appliances getting affected",
    "Want to know about solar power connection process",
    "Electricity bill not received this month",
    "Need help understanding tariff rates",
    "Street light not working in our lane",
    "Request for load enhancement in connection",
    "Meter display not visible, need replacement",
    "Want to avail subsidy for electricity bill",
    "Minor power cut for 1-2 hours daily",
    "Need information about online payment options",
    "Electricity connection transfer due to house sale",
    "Query about peak hour charges",
    "Request for LED street light installation",
    "Need clarification on fuel adjustment charges",
    "Want to install rooftop solar panels",
    "Electricity bill payment not reflecting",
    "Request for time of day meter installation",
    "Need help with net metering application",
    "Electricity connection for EV charging station",
    "Want to know about green energy options",
    "Request for underground cabling in area",
    "Need information about demand response program",
    "Electricity meter testing request",
    "Want to add another meter for separate unit",
    "Request for smart meter installation",
    "Need help with electricity subsidy renewal",
    "Query about electricity rebate scheme",
    "Electricity bill dispute for vacant property",
    "Want to change billing address",
    "Request for temporary power connection",
    "Need information about industrial tariff",
    "Electricity connection for agricultural pump"
]

WATER_HIGH = [
    "No water in tap for 3 days, emergency situation",
    "Pipe burst on main road, water flooding everywhere",
    "Water is muddy and brown, health hazard",
    "Contaminated water supply causing illness in area",
    "Main water pipeline leaked, entire street flooded",
    "No drinking water available, children suffering",
    "Water tank overflow causing road damage",
    "Sewage mixing with drinking water supply, dangerous",
    "Water pressure too high, pipes bursting",
    "No water supply in hospital area, critical",
    "Groundwater contamination suspected, testing needed",
    "Water logging due to broken pipeline, mosquito breeding",
    "Drinking water has foul smell, people getting sick",
    "Major leak in underground water main, sinkhole risk",
    "No water for firefighting system in building",
    "Water supply completely stopped since week",
    "Contaminated water causing skin diseases",
    "Burst pipe near electrical substation, electrocution risk",
    "Water scarcity affecting elderly residents badly",
    "Sewage backflow into water supply line, health emergency",
    "Water main break flooding basement apartments",
    "Drinking water turning hair green, copper contamination",
    "Water supply truck overturning, no alternative arrangement",
    "Pipeline rupture causing traffic chaos on highway",
    "Water contamination from chemical factory runoff",
    "No water for dialysis center, patients at risk",
    "Water pressure so low fire hydrants useless",
    "Broken water main washing away road foundation",
    "Water supply interrupted during heat wave, dehydration risk",
    "Contaminated well water causing mass poisoning",
    "Water pipeline passing through sewage line, cross contamination",
    "No water in maternity ward, new mothers suffering",
    "Water supply cut without notice, elderly stranded",
    "Burst water pipe damaging historical monument foundation",
    "Water contamination from agricultural pesticide runoff",
    "No water for school midday meal program",
    "Water supply line damaged by construction work",
    "Contaminated water causing diarrhea in children",
    "Water tank cracked, debris falling into supply",
    "No water for livestock, animals dying of thirst"
]

WATER_LOW = [
    "Water pressure is low in morning hours",
    "Need to apply for new water connection",
    "Water bill amount seems high",
    "Request to change name on water bill",
    "Tap leaking continuously, wasting water",
    "Need information about water tariff rates",
    "Want to install water meter for individual flat",
    "Water supply timing needs adjustment",
    "Request for water tanker during maintenance",
    "Need duplicate water bill copy",
    "Water connection transfer due to property sale",
    "Query about rainwater harvesting scheme",
    "Minor leakage in common area pipeline",
    "Want to know water quality test results",
    "Request for pipeline cleaning in our area",
    "Water bill not received this month",
    "Need help with online water bill payment",
    "Garden water connection needs activation",
    "Water pressure fluctuates throughout day",
    "Request for water saving device installation",
    "Need information about water connection fees",
    "Want to register complaint about water wastage",
    "Request for borewell permission",
    "Need help with water meter reading correction",
    "Water connection for construction site",
    "Want to know about water conservation schemes",
    "Request for flushing system repair in public toilet",
    "Need information about water testing laboratory",
    "Water bill rebate for senior citizens",
    "Request for water connection for community center",
    "Need clarification on sewerage charges",
    "Want to apply for agricultural water connection",
    "Water meter not working, need replacement",
    "Request for water supply schedule change",
    "Need help with water connection for rental property",
    "Water filter installation request for community",
    "Query about water usage limits",
    "Request for water connection for small business",
    "Need information about water quality parameters",
    "Water connection transfer after inheritance"
]

WASTE_WATER_HIGH = [
    "Drainage blocked, sewage water entering homes",
    "Manhole overflow on main road, traffic hazard",
    "Garbage not collected for 2 weeks, health risk",
    "Sewage water stagnating, mosquito breeding ground",
    "Drainage system completely choked, backflow in toilets",
    "Garbage dumping near residential area, disease risk",
    "Sewage line broken, foul smell unbearable",
    "Waste water flowing on street, children playing there",
    "Overflowing garbage bin causing rodent infestation",
    "Drainage cover missing, accident risk at night",
    "Sewage contamination in playground area",
    "Garbage burning causing air pollution, breathing issues",
    "Waste water mixing with storm water drain, flooding",
    "Blocked drainage causing water logging in houses",
    "Hazardous waste dumped near school area",
    "Sewage overflow near food market, contamination risk",
    "Garbage collection vehicle not coming since days",
    "Drainage gas leak, toxic smell in area",
    "Medical waste found in public garbage bin, dangerous",
    "Sewage backup in basement apartments, health emergency",
    "Clogged sewer line causing toilet overflow in hospital",
    "Garbage pile attracting stray animals, rabies risk",
    "Sewage pipe burst under building foundation",
    "Waste water contaminating nearby lake, fish dying",
    "Blocked storm drain causing flash flooding",
    "Garbage truck accident spilling waste on highway",
    "Sewage treatment plant malfunction, raw sewage discharge",
    "Illegal dumping of industrial waste in residential drain",
    "Garbage fire spreading toxic fumes across neighborhood",
    "Sewage line collapse creating large sinkhole",
    "Waste water from slaughterhouse flowing untreated",
    "Garbage accumulation causing dengue outbreak",
    "Sewage overflow contaminating vegetable market",
    "Blocked drainage causing malaria outbreak",
    "Garbage leachate polluting groundwater supply",
    "Sewage backup in old age home, residents evacuated",
    "Waste water from chemical lab entering municipal drain",
    "Garbage dump near temple, devotees suffering",
    "Sewage line damaged by tree roots, repeated blockages",
    "Waste accumulation causing cholera cases in slum"
]

WASTE_WATER_LOW = [
    "Garbage collection time needs to be earlier",
    "Request for additional garbage bins in area",
    "Street cleaning frequency should increase",
    "Need information about waste segregation rules",
    "Bulk waste disposal request for house renovation",
    "Garden waste not being collected separately",
    "Request for recycling bin installation",
    "Garbage bin lid broken, needs replacement",
    "Want to know about composting scheme",
    "E-waste collection drive needed in area",
    "Minor drainage slow drainage issue",
    "Request for awareness program on waste management",
    "Need larger garbage bin for apartment complex",
    "Plastic waste accumulation in nearby drain",
    "Want information about hazardous waste disposal",
    "Garbage sorting guidelines needed",
    "Request for more frequent street sweeping",
    "Construction debris removal needed",
    "Want to report illegal dumping spot",
    "Need help with bulk item disposal",
    "Request for organic waste converter installation",
    "Need information about plastic waste recycling",
    "Garbage bin placement causing traffic issue",
    "Request for community composting facility",
    "Need separate collection for paper waste",
    "Want to organize neighborhood cleanup drive",
    "Request for battery recycling drop box",
    "Need information about waste to energy program",
    "Garbage collection missed our street today",
    "Request for covered garbage bin installation",
    "Need clarification on bulk waste charges",
    "Want to report overflowing public bin",
    "Request for waste collection schedule change",
    "Need information about furniture disposal",
    "Garbage truck damaging road surface",
    "Request for more sanitation workers",
    "Need separate bin for glass waste",
    "Want to know about textile recycling",
    "Request for drain cleaning before monsoon",
    "Need information about waste reduction tips"
]

BILLING_HIGH = [
    "Electricity bill Rs.50000 for single month, clearly error",
    "Being charged for electricity after connection disconnected",
    "Double billing for same month, need immediate correction",
    "Penalty charged wrongly, account blocked unfairly",
    "Bill generated for vacant property, no usage at all",
    "Meter replaced but old meter readings still being billed",
    "Being charged commercial rates for residential connection",
    "Water bill shows 10000 units usage, impossible for family",
    "Disconnection notice received despite payment made",
    "Fraudulent charges appearing in bill, investigation needed",
    "Bill amount increased 10 times without any reason",
    "Being billed for neighbor's electricity usage",
    "Payment not reflected in system, wrongful disconnection threat",
    "Meter reading fake, actual reading much lower",
    "Charged for services not received in our area",
    "Bill generated without actual meter reading, inflated",
    "Tax charged twice in same bill, need refund",
    "Connection shows active but building demolished years ago",
    "Being charged maintenance fee for non-existent facility",
    "Utility bill causing financial hardship, clearly erroneous",
    "Billing error causing credit score damage",
    "Wrong meter number on bill, paying for stranger",
    "Estimated billing way too high, actual usage minimal",
    "Being charged for stolen electricity by others",
    "Bill shows usage when meter was under testing",
    "Arrears added wrongly despite full payment",
    "Being billed for dead relative's account",
    "Duplicate connection charges levied unfairly",
    "Late fee charged when payment was on time",
    "Bill amount higher than property rental value",
    "Being charged for three phase when single phase installed",
    "Wrong tariff category applied, commercial instead of residential",
    "Billing system showing unpaid when receipt generated",
    "Being charged for street light maintenance separately",
    "Bill includes charges for disconnected appliances",
    "Wrong zone billing, paying for different area",
    "Being charged premium rates without notification",
    "Bill shows negative balance, refund not processed",
    "Being billed for temple when Hindu household",
    "Utility bill sent to tenant instead of owner"
]

BILLING_LOW = [
    "Need payment plan for electricity bill",
    "Want to switch to auto-debit for bill payment",
    "Bill due date extension request",
    "Need clarification on fuel adjustment charges",
    "Request for bill breakdown explanation",
    "Want to receive bill via email instead of post",
    "Need help with subsidy application",
    "Query about late payment fee calculation",
    "Want to link multiple accounts for single payment",
    "Request for paperless billing enrollment",
    "Need information about senior citizen discount",
    "Bill payment receipt not generated",
    "Want to change billing cycle from monthly to bimonthly",
    "Query about security deposit refund",
    "Need help with bill dispute process",
    "Want to add tenant name to bill",
    "Request for consolidated bill for all utilities",
    "Need information about payment gateway charges",
    "Want to update mobile number for bill alerts",
    "Query about minimum bill amount",
    "Need information about installment options",
    "Want to know about early payment discount",
    "Request for duplicate receipt for tax purpose",
    "Need clarification on meter rent charges",
    "Want to avail paperless billing incentive",
    "Query about electricity duty charges",
    "Need help with online payment troubleshooting",
    "Want to change payment date to salary day",
    "Request for bill reminder via SMS",
    "Need information about UPI payment options",
    "Want to register for e-bill subscription",
    "Query about rebate for timely payment",
    "Need help with payment allocation across bills",
    "Want to know about wallet payment cashback",
    "Request for bill history for loan application",
    "Need clarification on fixed charges component",
    "Want to opt for green tariff billing",
    "Query about bill adjustment for outage days",
    "Need information about corporate payment portal",
    "Want to set up standing instructions for payment"
]


def generate_timestamp(start_date: datetime, end_date: datetime) -> str:
    """Generate a random timestamp between start and end dates."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    random_date = start_date + timedelta(days=random_days, seconds=random_seconds)
    return random_date.strftime("%Y-%m-%d %H:%M:%S")


def generate_complaint_data(num_complaints: int = 1500) -> List[Tuple]:
    """
    Generate synthetic complaint data with realistic patterns.
    
    Args:
        num_complaints: Number of complaint records to generate
        
    Returns:
        List of tuples containing complaint data
    """
    # Department data with templates and weights
    departments = [
        ("Electricity", ELECTRICITY_HIGH, ELECTRICITY_LOW, 0.40),
        ("Water Supply", WATER_HIGH, WATER_LOW, 0.35),
        ("Waste-Water/Sewage", WASTE_WATER_HIGH, WASTE_WATER_LOW, 0.25)
    ]
    
    # Status options with weights
    statuses = ["Pending", "In Progress", "Resolved", "Closed"]
    status_weights = [0.35, 0.25, 0.30, 0.10]
    
    complaints = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    # Add location modifiers for more realistic text
    locations = [
        "in Sector 12", "near City Hospital", "on MG Road", "in Gandhi Nagar",
        "near Central Park", "in Industrial Area", "near Railway Station",
        "in Old City", "near Shopping Mall", "in Residential Colony",
        "near School Zone", "in Commercial Complex", "near Bus Stand",
        "in VIP Area", "near Market Square"
    ]
    
    urgency_additions = [
        "Please resolve urgently", "Immediate action needed",
        "Very serious issue", "Hope for quick resolution",
        "Facing lot of problems", "Request immediate visit",
        "This is urgent", "Need help ASAP"
    ]
    
    for i in range(num_complaints):
        # Select department based on weights
        dept_choice = random.choices(departments, weights=[d[3] for d in departments])[0]
        department = dept_choice[0]
        high_templates = dept_choice[1]
        low_templates = dept_choice[2]
        
        # Severity distribution: ~40% High, ~60% Low
        is_high_severity = random.random() < 0.40
        
        if is_high_severity:
            severity = "High"
            base_text = random.choice(high_templates)
            # Add urgency keywords more often for high severity
            if random.random() < 0.5:
                base_text += " - " + random.choice(urgency_additions)
        else:
            severity = "Low"
            base_text = random.choice(low_templates)
        
        # Add location to some complaints for variety
        if random.random() < 0.6:
            base_text += " " + random.choice(locations)
        
        # Generate timestamp and status
        timestamp = generate_timestamp(start_date, end_date)
        
        # Status correlates with severity (High severity more likely to be Pending/In Progress)
        if severity == "High":
            status = random.choices(
                statuses,
                weights=[0.45, 0.30, 0.20, 0.05]
            )[0]
        else:
            status = random.choices(
                statuses,
                weights=[0.25, 0.20, 0.40, 0.15]
            )[0]
        
        complaint_id = f"CF-{10000 + i}"
        complaints.append((complaint_id, base_text, department, severity, timestamp, status))
    
    return complaints


def save_to_csv(complaints: List[Tuple], output_path: str) -> None:
    """Save complaint data to CSV file."""
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'text', 'department', 'severity', 'timestamp', 'status'])
        writer.writerows(complaints)
    
    print(f"Generated {len(complaints)} complaint records")
    print(f"Saved to: {output_path}")
    
    # Print distribution statistics
    dept_counts = {}
    severity_counts = {"High": 0, "Low": 0}
    status_counts = {}
    
    for _, text, dept, severity, _, status in complaints:
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
        severity_counts[severity] += 1
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\n=== Data Distribution ===")
    print("\nBy Department:")
    for dept, count in sorted(dept_counts.items()):
        print(f"  {dept}: {count} ({count/len(complaints)*100:.1f}%)")
    
    print("\nBy Severity:")
    for sev, count in severity_counts.items():
        print(f"  {sev}: {count} ({count/len(complaints)*100:.1f}%)")
    
    print("\nBy Status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count} ({count/len(complaints)*100:.1f}%)")


def main():
    """Main function to generate and save complaint data."""
    import sys
    
    print("=" * 60)
    print("CivicFix - Synthetic Complaint Data Generator")
    print("=" * 60)
    
    # Get number of complaints from command line or use default
    if len(sys.argv) > 1:
        try:
            num_complaints = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number. Using default: 50000")
            num_complaints = 50000
    else:
        num_complaints = 50000  # Default to 50000
    
    print(f"Generating {num_complaints:,} complaint records...")
    
    # Generate complaints
    complaints = generate_complaint_data(num_complaints)
    
    # Save to CSV (absolute path)
    import os
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "complaints_dataset.csv")
    save_to_csv(complaints, output_path)
    
    print("\n" + "=" * 60)
    print("Data generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
