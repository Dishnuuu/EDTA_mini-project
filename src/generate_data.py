"""
CivicFix - Synthetic Data Generator (IMPROVED QUALITY)
Generates 50,000+ realistic government utility complaint records with clear severity distinction.
Departments: Electricity, Water Supply, Waste-Water/Sewage, Billing & Accounts
Severity: High (urgent, dangerous, emergency, life-threatening) or Low (routine, inquiry, minor)

KEY IMPROVEMENTS:
- Much larger template variety (100 per category)
- Clearer severity keyword separation
- More realistic language patterns
- Better contextual variety with modifiers
"""

import csv
import random
from datetime import datetime, timedelta
from typing import List, Tuple


# ============================================================================
# HIGH SEVERITY TEMPLATES - URGENT/DANGEROUS/EMERGENCY
# Must contain: danger words, emergency terms, safety hazards, outages, flooding
# ============================================================================

ELECTRICITY_HIGH = [
    "COMPLETE BLACKOUT - entire area without power for 12+ hours, emergency",
    "No electricity since morning, hospital equipment affected, URGENT",
    "Total power failure in residential area, elderly people suffering",
    "Complete blackout affecting critical infrastructure, need immediate restoration",
    "Power cut during medical emergency, life support systems down",
    "Entire neighborhood dark for hours, food and medicine spoiling",
    "Electricity gone in extreme weather, children and elderly at risk",
    "Massive power outage affecting thousands of homes, emergency situation",
    "No power in ICU ward, patients on ventilator, CRITICAL",
    "Blackout in surgical center, operations halted, LIFE THREATENING",
    "FIRE HAZARD - transformer sparking and smoking, evacuation needed",
    "Electrical fire in meter box, flames visible, EMERGENCY",
    "Transformer exploded with loud bang, fire spreading rapidly",
    "Burning smell from electrical panel, smoke coming out, DANGER",
    "Electric pole on fire, melting and collapsing, URGENT",
    "Substation fire with thick black smoke, area evacuation needed",
    "Electrical short circuit causing sparks and flames, FIRE RISK",
    "Power box burning, plastic melting, toxic fumes spreading",
    "Transformer catching fire, explosion risk, CLEAR THE AREA",
    "Electrical room fire, spreading to nearby buildings, EMERGENCY",
    "LIVE WIRE hanging on road, ELECTROCUTION DANGER, stay away",
    "Electric shock from street pole, person hospitalized, DANGEROUS",
    "Exposed live cable after storm, DEADLY shock risk, URGENT",
    "High voltage wire snapped and lying on ground, LIFE THREATENING",
    "Electric pole leaning into trees, sparking dangerously, EMERGENCY",
    "Live wire touching metal fence, electrocution hazard, DANGER",
    "Downed power line across sidewalk, ACCIDENT RISK, keep away",
    "Electrical wire in waterlogged area, SHOCK HAZARD, emergency",
    "Sparking from electric pole, children playing nearby, DANGEROUS",
    "Broken wire with visible sparks, electrocution risk, URGENT",
    "Transformer destroyed in storm, complete area affected, EMERGENCY",
    "Electric pole crashed into building, structural damage, URGENT",
    "Power lines down across road, traffic accident risk, DANGER",
    "Electrical equipment destroyed in flood, major hazard, EMERGENCY",
    "Substation damaged by lightning, no power restoration yet",
    "Main distribution box melted and burnt, FIRE RISK",
    "Electric pole broken in half, about to collapse, DANGEROUS",
    "Power cable severed, exposed conductors visible, SHOCK RISK",
    "Transformer oil leaking, explosion imminent, EVACUATE AREA",
    "Electrical panel completely burnt, wiring exposed, HAZARD",
    "EXTREME voltage fluctuation, all appliances burning out, URGENT",
    "Dangerous power surge damaging everything connected, EMERGENCY",
    "Very high voltage causing fires in multiple homes, DANGER",
    "Massive power surge destroyed expensive equipment, major loss",
    "Voltage spike causing electrical fires, multiple incidents reported",
    "Overvoltage burning motors and ACs, severe damage ongoing",
    "Power fluctuation causing equipment explosions, HAZARD",
    "Dangerous voltage levels, fire risk in every home, URGENT",
    "Extreme voltage variation, electronics catching fire, EMERGENCY",
    "High tension causing sparks and burning, LIFE THREATENING",
    "Electrical room flooded, major electrocution hazard, DANGER",
    "Power lines touching during storm, massive spark shower, EMERGENCY",
    "Electricity meter exploding, glass shards flying everywhere",
    "Underground cable explosion, manhole cover blown off road",
    "High voltage arc between lines, loud booming, PANIC in area",
    "Electric shock from water pipe, entire plumbing electrified",
    "Short circuit in elevator, people trapped inside, RESCUE NEEDED",
    "Electrical fire in hospital, patients being evacuated, CRITICAL",
    "Power failure in neonatal unit, newborns at risk, EMERGENCY",
    "Electrocution death in area, same fault still active, DANGER",
    "Power lines fallen on car, occupants getting shocks, RESCUE",
    "Electrical explosion injured multiple people, AMBULANCE NEEDED",
    "Transformer burning with loud noise, area shaking, PANIC",
    "Live wire in playground, children at risk of death, URGENT",
    "Electric pole falling on house, family trapped inside, RESCUE",
    "Massive electrical fire spreading to homes, FIRE BRIGADE NEEDED",
    "Power line collapse blocking emergency vehicle route, DANGER",
    "Electrical hazard causing road collapse, vehicles falling, URGENT",
    "Sparking transformer near gas station, EXPLOSION RISK, EVACUATE",
    "Electricity causing water contamination, health emergency, DANGER",
]

WATER_HIGH = [
    "NO WATER for 5+ days, severe dehydration risk, EMERGENCY",
    "Complete water supply failure, hospital affected, CRITICAL",
    "Zero water pressure for days, people buying expensive tankers",
    "No drinking water in entire area, health crisis developing",
    "Water supply stopped without notice, elderly and infants suffering",
    "Total water failure in heat wave, dehydration deaths reported",
    "No water for dialysis center, patients life at risk, URGENT",
    "Dry taps for week, sanitation impossible, DISEASE RISK",
    "Water supply completely dead, maternity ward affected, EMERGENCY",
    "No water in school, children sent home, health hazard",
    "MASSIVE pipe burst flooding entire street, water entering homes",
    "Main water line exploded, road washing away, URGENT",
    "Burst pipe creating huge water flow, property damage severe",
    "Water main break causing flash flooding, evacuation needed",
    "Pipeline rupture flooding basement apartments, people trapped",
    "Huge geyser from broken pipe, entire area waterlogged, EMERGENCY",
    "Water pipe burst under road, sinkhole forming, DANGER",
    "Major leak flooding electrical substation, electrocution risk",
    "Broken water main destroying road foundation, URGENT",
    "Pipeline explosion damaging nearby buildings, EMERGENCY",
    "CONTAMINATED water causing mass illness, people hospitalized",
    "Sewage mixing with drinking water, HEALTH EMERGENCY",
    "Toxic chemicals in water supply, poisoning reported, DANGER",
    "Brown foul-smelling water causing vomiting and diarrhea",
    "Water contaminated with bacteria, cholera outbreak starting",
    "Poisoned water supply affecting hundreds, EMERGENCY declared",
    "Dirty sewage in drinking water, skin diseases spreading",
    "Water has chemical taste, people getting sick, URGENT",
    "Contaminated water causing hepatitis outbreak, CRITICAL",
    "Fecal contamination in water supply, health emergency, DANGER",
    "Water contamination causing children to fall seriously ill",
    "Toxic water supply leading to kidney problems, URGENT",
    "Polluted water causing mass skin infections, hospital full",
    "Dangerous bacteria in water, typhoid cases rising, EMERGENCY",
    "Water quality so bad its burning skin, chemical contamination",
    "Hazardous water supply affecting pregnant women, CRITICAL",
    "Contaminated water causing liver damage in residents, URGENT",
    "Poisonous water leading to neurological symptoms, DANGER",
    "Water supply infected with deadly pathogens, EMERGENCY",
    "Toxic algae in water reservoir, poisoning people, URGENT",
    "Water tank collapsing, will flood entire area, EVACUATE",
    "Damaged water treatment plant, raw sewage discharge, EMERGENCY",
    "Water pipeline passing through sewage, cross contamination, DANGER",
    "Major water infrastructure failure affecting thousands, URGENT",
    "Water treatment facility destroyed, contamination risk, EMERGENCY",
    "Broken water infrastructure causing sanitation crisis, DANGER",
    "Water supply system completely failed, humanitarian crisis",
    "Critical water infrastructure damaged, public health emergency",
    "Water network failure causing disease outbreak, URGENT",
    "Major water system collapse, area without water for weeks",
    "Water shortage causing riots in area, law and order issue",
    "No water for firefighting, buildings at risk, DANGEROUS",
    "Water crisis leading to severe dehydration deaths, EMERGENCY",
    "Contaminated water killing livestock, livelihood threat, URGENT",
    "Water emergency in slum area, children dying, CRITICAL",
    "No water for sanitation workers, health hazard spreading",
    "Water failure in old age home, elderly suffering, URGENT",
    "Contaminated water causing miscarriages, women hospitalized",
    "Water crisis causing mass migration from area, EMERGENCY",
    "No water in COVID care center, infection risk, CRITICAL",
]

WASTE_WATER_HIGH = [
    "SEWAGE overflowing into homes, toxic waste everywhere, EMERGENCY",
    "Manhole overflowing with sewage, flooding streets, HEALTH HAZARD",
    "Sewage water backflow in toilets, homes flooded with waste, URGENT",
    "Raw sewage flowing on roads, children playing in it, DANGER",
    "Sewer line burst flooding area with toxic waste, EVACUATE",
    "Massive sewage overflow contaminating playground, HEALTH RISK",
    "Sewage water entering bedrooms and kitchens, TOXIC, URGENT",
    "Overflowing sewage creating health emergency in area, DANGER",
    "Sewage flood destroying property, contamination severe, EMERGENCY",
    "Raw sewage flowing from manholes, disease outbreak risk, URGENT",
    "COMPLETELY blocked drainage causing flooding, emergency situation",
    "Sewer line totally choked, sewage backing up everywhere, URGENT",
    "Drainage system 100 percent blocked, water logging severe, DANGER",
    "Totally clogged sewer causing toilet overflows in hospital, CRITICAL",
    "Blocked main drain flooding entire neighborhood, EMERGENCY",
    "Sewage blockage causing health crisis in area, URGENT",
    "Complete drainage failure, sewage everywhere, HEALTH HAZARD",
    "Blocked sewer creating toxic gas leak, breathing difficulty, DANGER",
    "Drainage totally jammed, waste water rising in homes, EMERGENCY",
    "Sewer completely blocked, raw sewage on streets, URGENT",
    "HAZARDOUS medical waste in public area, needle sticks reported, DANGER",
    "Garbage not collected for month, disease outbreak starting",
    "Toxic industrial waste dumped in residential drain, POISONING",
    "Infected hospital waste mixed with garbage, health emergency",
    "Dangerous chemical waste leaking into groundwater, URGENT",
    "Biohazard waste in public bin, children exposed, DANGER",
    "Radioactive waste improperly disposed, contamination risk, EMERGENCY",
    "Sharp medical waste causing injuries to sanitation workers",
    "Infectious waste spreading disease in area, health crisis",
    "Hazardous waste causing birth defects in area, URGENT",
    "Sewage contamination causing cholera outbreak, deaths reported",
    "Garbage accumulation leading to dengue epidemic, EMERGENCY",
    "Stagnant sewage creating malaria outbreak, hospital overwhelmed",
    "Waste water contamination causing typhoid epidemic, URGENT",
    "Garbage dump causing hepatitis outbreak, children dying",
    "Sewage pollution leading to dysentery epidemic, CRITICAL",
    "Waste contamination causing jaundice outbreak, many hospitalized",
    "Garbage breeding mosquitoes, dengue deaths increasing, EMERGENCY",
    "Sewage causing leptospirosis outbreak, people dying, URGENT",
    "Toxic waste causing cancer cluster in area, health emergency",
    "Sewage flowing directly into river, mass fish deaths, ECOLOGICAL DISASTER",
    "Waste water contaminating drinking water source, EMERGENCY",
    "Raw sewage polluting lake, water supply threatened, URGENT",
    "Garbage leachate poisoning groundwater, health crisis, DANGER",
    "Sewage treatment plant failure, raw waste in environment, EMERGENCY",
    "Toxic waste killing all aquatic life, ecological disaster, URGENT",
    "Sewage contaminating agricultural fields, food safety risk",
    "Waste water destroying wetland ecosystem, environmental emergency",
    "Garbage fire creating toxic air pollution, breathing hazard, DANGER",
    "Sewage spill destroying natural habitat, wildlife dying, URGENT",
    "Missing manhole cover in dark area, people falling in, DEATHS",
    "Sewage gas explosion in building, multiple injuries, EMERGENCY",
    "Garbage landslide burying nearby homes, rescue needed, URGENT",
    "Toxic waste fire spreading poisonous smoke, EVACUATE AREA",
    "Sewage line collapse creating massive sinkhole, buildings at risk",
    "Waste accumulation causing building collapse, deaths reported",
    "Sewer gas leak causing mass unconsciousness, hospital emergency",
    "Garbage dump fire releasing toxic fumes, respiratory emergency",
    "Sewage contamination making area uninhabitable, evacuation needed",
    "Waste water flooding causing structural damage to hospital, URGENT",
]

BILLING_HIGH = [
    "BILL ERROR: Charged 50000 rupees for 500 usage, CLEAR SYSTEM ERROR",
    "Massive billing mistake - 100000 for vacant property, IMPOSSIBLE",
    "WRONG BILL: 100x normal amount, obviously computer error, URGENT",
    "Charged 80000 for unused connection, FRAUD or ERROR, URGENT",
    "Bill shows 150000 for single month, IMPOSSIBLE amount, ERROR",
    "Extremely wrong billing - 60000 when usage is zero, ERROR",
    "Absurd bill of 120000 for empty building, CLEAR MISTAKE",
    "Wrong bill 90000 for disconnected service, REFUND NEEDED",
    "Ridiculous charge of 70000, never used that much, SYSTEM ERROR",
    "Impossible bill 200000, higher than property value, ERROR",
    "DOUBLE BILLED for same month, paid twice, need immediate refund",
    "FRAUDULENT charges on account, did not use these services, URGENT",
    "Being charged for neighbor usage, billing mix-up, ERROR",
    "Fake meter readings generating false bills, FRAUD happening",
    "Charged for services after disconnection, WRONG billing, URGENT",
    "Multiple bills for same period, system error, REFUND NEEDED",
    "Being billed for stolen electricity by others, NOT MY USAGE",
    "Fraudulent account created in my name, IDENTITY THEFT, URGENT",
    "Charged for three connections when only one exists, ERROR",
    "Ghost charges appearing in bill, ACCOUNT TAMPERING, URGENT",
    "COMMERCIAL rates applied to home, 5x normal bill, ERROR",
    "Wrong tariff category causing massive overcharge, URGENT",
    "Being charged industrial rates for residence, WRONG, ERROR",
    "Premium rates applied without notice, bill inflated 8x, ERROR",
    "Incorrect rate causing financial hardship, CLEAR MISTAKE, URGENT",
    "Charged premium tariff when eligible for subsidy, WRONG",
    "Wrong billing category making bill unaffordable, ERROR",
    "Commercial tariff on residential connection, HUGE error, URGENT",
    "Being charged wrong rate, bill increased 6x, SYSTEM ERROR",
    "Incorrect pricing applied, bill is fraudulent, ERROR, URGENT",
    "PAYMENT NOT REFLECTING despite proof, wrongful disconnection threat, URGENT",
    "Paid bill but showing unpaid, harassment for non-payment, ERROR",
    "Account blocked despite full payment, FINANCIAL DAMAGE, URGENT",
    "Wrongful late fees charging hundreds, payment was on time, ERROR",
    "Being penalized for late payment when paid early, INJUSTICE",
    "Payment receipt ignored, being threatened with disconnection, URGENT",
    "Bank deduction made but bill showing unpaid, ERROR, URGENT",
    "Auto-debit failed but bank charged, double payment issue, ERROR",
    "Online payment not updated in system, harassment, URGENT",
    "Paid through app but bill still overdue, PROOF AVAILABLE, ERROR",
    "WRONGFUL disconnection notice, bill is clearly erroneous, URGENT",
    "Threatened with disconnection for bill I did not owe, ERROR",
    "Disconnection notice for paid account, HARASSMENT, URGENT",
    "Being disconnected despite payment, FINANCIAL LOSS, ERROR",
    "Wrongful disconnection threat for disputed bill, INJUSTICE",
    "Power cut notice for incorrect bill, MENTAL HARASSMENT, URGENT",
    "Disconnection threatened for system error bill, ERROR, URGENT",
    "Service cut despite paying correct amount, HARASSMENT, ERROR",
    "Wrongful disconnection causing business loss, CLAIM PENDING",
    "Disconnected for wrong bill, emergency restoration needed, URGENT",
    "Billing error destroying credit score, FINANCIAL DAMAGE, URGENT",
    "Wrong bill causing loan rejection, LIFE IMPACT, ERROR",
    "Erroneous billing affecting business operations, FINANCIAL LOSS",
    "Incorrect bill causing mental harassment, HEALTH IMPACT, URGENT",
    "Billing mistake leading to legal issues, DEFAMATION, ERROR",
    "Wrong charges causing bankruptcy, LIVELIHOOD DESTROYED, URGENT",
    "Bill error affecting children education funds, FAMILY CRISIS",
    "Incorrect billing causing depression, MENTAL HEALTH IMPACT",
    "Fraudulent bill leading to court case, LEGAL HARASSMENT, URGENT",
    "Billing error causing job loss, CAREER DAMAGE, ERROR",
]

# ============================================================================
# LOW SEVERITY TEMPLATES - ROUTINE/MINOR/INQUIRY
# Must contain: inquiry words, request terms, minor issues, information seeking
# ============================================================================

ELECTRICITY_LOW = [
    "Question about electricity bill calculation and charges",
    "Need clarification on monthly electricity bill amount",
    "Understanding electricity tariff rates for residential use",
    "Query about electricity bill payment methods available",
    "Information needed on electricity billing cycle dates",
    "How to read electricity meter and calculate usage",
    "Question about peak hour electricity charges",
    "Need help understanding electricity bill components",
    "Clarification on fuel adjustment charge in bill",
    "Information about electricity tax and duties",
    "Request for new electricity connection in residential area",
    "Application for additional electricity connection needed",
    "Want to apply for three phase electricity connection",
    "New electricity connection for recently constructed building",
    "Request for temporary electricity connection for event",
    "Need electricity connection for commercial establishment",
    "Application for agricultural electricity connection",
    "Request for industrial electricity connection setup",
    "Need temporary power connection for construction work",
    "Electricity connection request for community hall",
    "Need to update name on electricity bill account",
    "Request to change address on electricity connection",
    "Want to transfer electricity connection to new owner",
    "Update phone number for electricity bill notifications",
    "Change email address for electricity bill delivery",
    "Request for electricity account name correction",
    "Need to update ownership details for connection",
    "Want to modify electricity connection details",
    "Request to update meter details in electricity account",
    "Need to change billing address for electricity",
    "Street light not working properly in our lane",
    "Occasional flickering in street lamp near home",
    "Minor power fluctuation affecting some appliances",
    "Electricity meter display not clearly visible",
    "Request for street light repair in neighborhood",
    "Power cut for 1-2 hours during scheduled maintenance",
    "Need electricity meter cover replacement",
    "Street light timing needs adjustment",
    "Minor electrical issue in common area",
    "Request for meter box cleaning and maintenance",
    "Small spark from switch occasionally, probably loose connection",
    "Minor wiring issue in outlet, needs inspection when convenient",
    "Slight burning smell from old appliance, not electrical system",
    "Small electrical flicker in one room, minor issue",
    "Light sparking from old socket, needs replacement routine",
    "Minor electrical buzzing from doorbell, low priority",
    "Small power dip in one outlet, probably overloaded strip",
    "Slight flickering in ceiling fan light, minor fix needed",
    "Information about solar panel installation process",
    "Query about net metering for rooftop solar",
    "Need details about electricity subsidy schemes",
    "How to apply for electricity connection online",
    "Information about green energy options available",
    "Query about electricity rebate programs",
    "Need information on time-of-day metering",
    "How to get duplicate electricity bill copy",
    "Information about electricity connection fees",
    "Query about smart meter installation process",
    "Need help with online electricity bill payment",
    "Question about electricity bill payment receipt",
    "How to set up auto-debit for electricity bill",
    "Information about electricity payment centers",
    "Query about electricity bill payment extension",
    "Need electricity payment plan information",
    "How to pay electricity bill through mobile app",
    "Information about electricity bill discount schemes",
    "Query about electricity security deposit refund",
    "Need help with electricity payment issue",
    "Request for electricity bill via email instead of post",
    "Want to enroll in paperless electricity billing",
    "Need electricity bill history for tax purposes",
    "Query about electricity connection transfer process",
    "Information about load enhancement for connection",
    "Request for electricity meter testing service",
    "Need clarification on electricity minimum charges",
    "How to apply for electricity subsidy as senior citizen",
    "Query about electricity meter rent charges",
    "Information about electricity demand response program",
]

WATER_LOW = [
    "Question about water bill calculation and charges",
    "Need clarification on monthly water bill amount",
    "Understanding water tariff rates for residential use",
    "Query about water bill payment methods available",
    "Information needed on water billing cycle dates",
    "How to read water meter and calculate usage",
    "Question about water service charges",
    "Need help understanding water bill components",
    "Clarification on sewerage charges in water bill",
    "Information about water tax and fees",
    "Request for new water connection in residential area",
    "Application for additional water connection needed",
    "Want to apply for commercial water connection",
    "New water connection for recently built property",
    "Request for temporary water connection for event",
    "Need water connection for commercial space",
    "Application for agricultural water connection",
    "Request for industrial water connection setup",
    "Need temporary water connection for construction",
    "Water connection request for community facility",
    "Need to update name on water bill account",
    "Request to change address on water connection",
    "Want to transfer water connection to new owner",
    "Update phone number for water bill notifications",
    "Change email for water bill delivery",
    "Request for water account name correction",
    "Need to update ownership details for water",
    "Want to modify water connection details",
    "Request to update meter details in water account",
    "Need to change billing address for water",
    "Water pressure slightly low during morning hours",
    "Minor tap leakage in common area pipeline, please check when convenient",
    "Water supply timing could be adjusted slightly",
    "Request for water meter reading correction",
    "Small leak in garden water connection, minor drip issue",
    "Water pressure fluctuates throughout the day",
    "Need water meter replacement due to age",
    "Request for pipeline cleaning in area",
    "Minor water pressure issue in building",
    "Water flow rate seems lower than usual",
    "Small water leak under sink, needs washer replacement",
    "Minor dripping from faucet, just annoying not urgent",
    "Slight leak in bathroom pipe, small puddle forming",
    "Water dripping slowly from shower head, minor issue",
    "Tiny leak in water tank, few drops per minute",
    "Minor seepage from pipe joint, not causing damage",
    "Small drip from water heater valve, routine fix needed",
    "Light leak in outdoor hose connection, low priority",
    "Water seeping slightly from valve, minor maintenance",
    "Slow drip from kitchen tap, washer probably needs replacing",
    "Information about water quality test results",
    "Query about rainwater harvesting installation",
    "Need details about water conservation schemes",
    "How to apply for water connection online",
    "Information about borewell permission process",
    "Query about water testing laboratory services",
    "Need information on water connection fees",
    "How to get duplicate water bill copy",
    "Information about water meter installation",
    "Query about water supply schedule in area",
    "Need help with online water bill payment",
    "Question about water bill payment receipt",
    "How to set up auto-debit for water bill",
    "Information about water payment centers",
    "Query about water bill payment options",
    "Need water payment plan information",
    "How to pay water bill through app",
    "Information about water bill assistance programs",
    "Query about water deposit refund process",
    "Need help with water payment issue",
    "Request for water bill via email delivery",
    "Want to enroll in paperless water billing",
    "Need water bill history for records",
    "Query about water connection transfer process",
    "Information about water load enhancement",
    "Request for water meter calibration",
    "Need clarification on water minimum charges",
    "How to apply for water subsidy",
    "Query about water service fees",
    "Information about water conservation rebates",
]

WASTE_WATER_LOW = [
    "Request for additional garbage bins in area",
    "Need more frequent garbage collection service",
    "Want to schedule bulk waste pickup for renovation",
    "Request for garden waste collection service",
    "Need information about e-waste disposal options",
    "Request for recycling bin installation nearby",
    "Want to organize neighborhood cleanup drive",
    "Need larger garbage bin for apartment complex",
    "Request for covered garbage bin installation",
    "Need separate collection for paper waste",
    "Garbage bin lid broken and needs replacement",
    "Minor drainage slow in our street area",
    "Garbage collection missed our street today",
    "Request for more frequent street sweeping",
    "Garbage truck damaging road surface slightly",
    "Need garbage bin placement adjustment",
    "Request for drain cleaning before monsoon",
    "Minor issue with garbage sorting guidelines",
    "Garbage collection timing could be earlier",
    "Small drainage cover needs repair",
    "Information about waste segregation guidelines",
    "Query about composting scheme availability",
    "Need details about hazardous waste disposal",
    "How to dispose of construction debris properly",
    "Information about plastic waste recycling",
    "Query about furniture disposal options",
    "Need information on textile recycling programs",
    "How to participate in waste reduction",
    "Information about battery recycling drop-off",
    "Query about waste-to-energy programs",
    "Request for community composting facility",
    "Want awareness program on waste management",
    "Need separate bin for glass waste collection",
    "Request for organic waste converter installation",
    "Want to report illegal dumping location",
    "Need information about bulk item disposal",
    "Request for waste collection schedule change",
    "Want more sanitation workers in area",
    "Need clarification on bulk waste charges",
    "Request for neighborhood waste education",
    "Garbage bin needs cleaning and sanitization",
    "Request for drainage inspection and cleaning",
    "Need minor repair to storm water drain",
    "Garbage collection vehicle route optimization",
    "Request for bin area pavement repair",
    "Need drainage grate replacement in area",
    "Minor sewer line inspection requested",
    "Request for waste bin repainting",
    "Need drain de-silting in neighborhood",
    "Garbage station needs minor maintenance",
    "Small amount of water stagnating in yard, minor mosquito concern",
    "Minor sewage smell near drain, occasional not constant",
    "Slight garbage odor from bin area, routine cleaning needed",
    "Small drainage blockage in one spot, minor issue",
    "Light sewage odor after rain, dissipates quickly",
    "Minor garbage accumulation in corner, needs sweeping",
    "Small amount of standing water in drain, not flooding",
    "Slight waste buildup in gutter, routine cleanup",
    "Minor drainage slowdown in one section, low priority",
    "Small sewage seepage from old pipe, minor maintenance",
    "Query about waste collection fees",
    "Information about composting workshop dates",
    "Need waste disposal guidelines pamphlet",
    "Request for waste management newsletter",
    "Query about recycling center locations",
    "Information about waste reduction tips",
    "Need clarification on waste collection rules",
    "Request for waste bin quantity increase",
    "Query about special waste pickup service",
    "Information about community cleanup events",
]

BILLING_LOW = [
    "Question about electricity bill payment methods",
    "Need help with online bill payment process",
    "How to set up automatic bill payment",
    "Information about bill payment centers nearby",
    "Query about bill payment receipt generation",
    "Need bill payment plan options information",
    "How to pay bill through mobile application",
    "Information about payment gateway charges",
    "Query about minimum bill payment amount",
    "Need help with payment allocation across bills",
    "Query about bill calculation methodology",
    "Need clarification on fixed charges component",
    "Understanding bill breakdown and components",
    "Information about tariff rates and slabs",
    "Query about meter rent charges on bill",
    "Need explanation of fuel adjustment charges",
    "Information about electricity duty charges",
    "Query about tax components in bill",
    "Need bill dispute process information",
    "How to request bill audit and verification",
    "Request to update contact number for bills",
    "Need to change billing address on account",
    "Want to update email for bill notifications",
    "Request for name correction on bill",
    "Need to update account ownership details",
    "Want to add tenant name to bill account",
    "Request for account details modification",
    "Need to link multiple accounts together",
    "Want to update billing preferences",
    "Request for account information update",
    "Want to receive bill via email instead of post",
    "Request for paperless billing enrollment",
    "Need to change billing cycle preference",
    "Want consolidated bill for all utilities",
    "Request for bill reminder via SMS",
    "Need to set up e-bill subscription",
    "Want to opt for green tariff billing",
    "Request for bill history access",
    "Need to update billing communication preference",
    "Want to register for bill alert service",
    "Information about senior citizen bill discount",
    "Query about early payment rebate options",
    "Need details about subsidy application process",
    "How to avail bill concession schemes",
    "Information about bill assistance programs",
    "Query about bill waiver eligibility",
    "Need information on bill support schemes",
    "How to apply for bill subsidy as farmer",
    "Information about bill discount for timely payment",
    "Query about bill rebate program details",
    "Need duplicate bill receipt for tax filing",
    "Request for bill breakdown explanation",
    "Query about security deposit refund process",
    "Information about installment payment options",
    "Need clarification on late fee calculation",
    "Request for bill adjustment information",
    "Query about bill correction process",
    "Need information about bill dispute resolution",
    "How to get bill correction for error",
    "Information about bill payment extension options",
    "Small billing error on account, few rupees wrong, please correct",
    "Minor discrepancy in bill amount, slight difference noticed",
    "Small wrong charge on bill, probably data entry error",
    "Minor billing mistake, amount slightly off, routine fix",
    "Small error in bill calculation, needs verification",
    "Slight discrepancy in meter reading on bill, minor correction",
    "Minor wrong entry in bill, probably typo error",
    "Small billing adjustment needed, amount slightly incorrect",
    "Minor dispute in bill charges, few items questionable",
    "Slight error in bill total, needs recalculation routine",
]

# ============================================================================
# ROADS & INFRASTRUCTURE TEMPLATES
# ============================================================================

ROADS_HIGH = [
    "MASSIVE pothole on main road, vehicles getting damaged, ACCIDENT RISK",
    "Huge crater in road, cars falling in, EMERGENCY repair needed",
    "Road completely collapsed, traffic blocked, URGENT",
    "Giant pothole causing accidents, people injured, DANGER",
    "Road caved in after rain, sinkhole forming, EVACUATE AREA",
    "Massive road damage, buses swerving to avoid, CRITICAL",
    "Deep pothole flipping motorcycles, hospital cases rising, URGENT",
    "Road surface destroyed, vehicles bottoming out, EMERGENCY",
    "Huge gap in road, children falling in, DANGER",
    "Road broken apart, complete blockage, URGENT restoration needed",
    "Bridge damage expanding, structural failure risk, EVACUATE",
    "Road washing away in rain, houses at risk, EMERGENCY",
    "Massive crack in overpass, collapse imminent, DANGER",
    "Road subsiding, underground cavity forming, CRITICAL",
    "Highway pothole causing pile-up accidents, multiple injuries, URGENT",
    "Road surface exploding, gas line suspected, EVACUATE",
    "Bridge joint broken, vehicles jumping, ACCIDENT RISK",
    "Road completely destroyed by flood, impassable, EMERGENCY",
    "Massive sinkhole swallowing cars, rescue needed, CRITICAL",
    "Road collapsing into drainage, buildings at risk, DANGER",
    "Pothole causing wheel damage, multiple vehicles affected, URGENT",
    "Road surface peeling off, skidding accidents, DANGER",
    "Highway crack spreading, entire road at risk, EMERGENCY",
    "Road giving way, underground erosion, CRITICAL situation",
    "Bridge railing collapsed, vehicles falling off, DEADLY",
    "Road surface melting, tar bubbling, BURN HAZARD",
    "Massive road depression forming, water accumulating, DANGER",
    "Road edge crumbling, vehicles falling off, URGENT",
    "Pothole causing brake failure accidents, deaths reported, CRITICAL",
    "Road completely impassable, ambulances can't reach, EMERGENCY",
    "Flyover pillar crack visible, structural collapse risk, DANGER",
    "Road surface shattered, glass-like cracking, URGENT",
    "Massive road heave, vehicles launching, ACCIDENT RISK",
    "Road collapsing near school, children at risk, EMERGENCY",
    "Highway pothole causing fatal accidents, deaths rising, CRITICAL",
    "Road surface disintegrating, gravel everywhere, DANGER",
    "Bridge expansion joint failed, gap widening, URGENT",
    "Road washing away, foundation exposed, EMERGENCY repair",
    "Massive pothole blocking entire lane, traffic chaos, URGENT",
    "Road surface sinking, underground pipe burst suspected, DANGER",
]

ROADS_LOW = [
    "Small pothole on side of road, minor inconvenience",
    "Minor crack in road surface, routine repair needed",
    "Small depression in road, slight bump when driving",
    "Minor road wear and tear, needs resurfacing eventually",
    "Small patch of road damaged, low priority fix",
    "Minor road edge deterioration, routine maintenance",
    "Small crack in sidewalk, trip hazard but minor",
    "Minor road marking faded, needs repainting sometime",
    "Small pothole forming, please fill when convenient",
    "Minor road surface roughness, uncomfortable but passable",
    "Request for road sweeping and cleaning in area",
    "Need speed bump installation near school, safety measure",
    "Request for road marking refresh in neighborhood",
    "Need street sign installation at intersection",
    "Request for pedestrian crossing marking on road",
    "Need minor road shoulder repair in area",
    "Request for drainage grate replacement on road",
    "Need road side mirror installation at blind curve",
    "Request for road name board installation",
    "Need minor footpath repair in neighborhood",
    "Small crack in footpath, needs filling routine",
    "Minor footpath unevenness, slight trip risk",
    "Request for footpath cleaning in area",
    "Need minor footpath edge repair, low priority",
    "Request for pedestrian path maintenance",
    "Small pothole in parking area, routine fix needed",
    "Minor road surface discoloration, cosmetic issue",
    "Request for road side vegetation trimming",
    "Need minor road drainage cleaning, slow drainage",
    "Request for road side barrier installation, routine",
    "Small road surface patch coming loose, minor issue",
    "Minor road camber issue, water pooling slightly",
    "Request for road side reflector installation",
    "Need minor road joint sealing, routine maintenance",
    "Request for road side guardrail inspection",
    "Small road surface blemish, cosmetic concern only",
    "Minor road side erosion, slight soil movement",
    "Request for road side ditch cleaning, routine",
    "Need minor road surface leveling, slight unevenness",
    "Request for road side tree trimming near path",
    "Small road crack sealing needed, routine maintenance",
    "Minor road surface texture issue, slightly rough",
    "Request for road side curb repair, minor damage",
    "Need minor road side slope adjustment, drainage issue",
    "Request for road side lighting improvement, dim area",
    "Small road patch work needed, wear and tear",
    "Minor road surface aging, routine resurfacing due",
    "Request for road side signage update, outdated signs",
    "Need minor road side barrier painting, faded",
    "Request for road side drainage cover replacement",
]


def generate_timestamp(start_date: datetime, end_date: datetime) -> str:
    """Generate a random timestamp between start and end dates."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    random_date = start_date + timedelta(days=random_days, seconds=random_seconds)
    return random_date.strftime("%Y-%m-%d %H:%M:%S")


def generate_complaint_data(num_complaints: int = 50000) -> List[Tuple]:
    """
    Generate synthetic complaint data with realistic patterns.

    Args:
        num_complaints: Number of complaint records to generate

    Returns:
        List of tuples containing complaint data
    """
    # Department data with templates and weights
    departments = [
        ("Electricity", ELECTRICITY_HIGH, ELECTRICITY_LOW, 0.28),
        ("Water Supply", WATER_HIGH, WATER_LOW, 0.24),
        ("Waste-Water/Sewage", WASTE_WATER_HIGH, WASTE_WATER_LOW, 0.16),
        ("Billing & Accounts", BILLING_HIGH, BILLING_LOW, 0.12),
        ("Roads & Infrastructure", ROADS_HIGH, ROADS_LOW, 0.20)
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

    # HIGH severity urgency additions (maintains urgency tone)
    high_urgency_additions = [
        "- Immediate action needed",
        "- URGENT please resolve",
        "- Emergency situation",
        "- Very serious issue",
        "- Request immediate action",
        "- This is critical",
        "- Need emergency response",
        "- Life threatening situation",
        "- Safety hazard, act now",
        "- Extreme urgency",
    ]

    # LOW severity polite additions (maintains routine tone)
    low_polite_additions = [
        "Please look into this when possible",
        "Thank you for your service",
        "Hope for a resolution soon",
        "Request your kind attention",
        "Would appreciate your help",
        "Please advise on next steps",
        "Looking forward to your response",
        "Kindly process this request",
        "Thank you for your assistance",
        "Please provide information",
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
            if random.random() < 0.4:
                base_text += " " + random.choice(high_urgency_additions)
        else:
            severity = "Low"
            base_text = random.choice(low_templates)
            # Add polite additions for low severity
            if random.random() < 0.3:
                base_text += " - " + random.choice(low_polite_additions)

        # Add location to some complaints for variety
        if random.random() < 0.5:
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
    print("CivicFix - Synthetic Complaint Data Generator (IMPROVED)")
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

    # Save to CSV (relative to project root)
    output_path = "../data/complaints_dataset.csv"
    save_to_csv(complaints, output_path)

    print("\n" + "=" * 60)
    print("Data generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
