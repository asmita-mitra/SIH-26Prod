import pandas as pd
import joblib
import random

from configur.mines import MINES

mine_name = input(
    "Enter Mine Name: "
).strip().lower()

mine_lookup = {
    name.lower(): data
    for name, data in MINES.items()
}

if mine_name not in mine_lookup:

    print("\nMine not found.")
    print("Available mines:")

    for name in MINES.keys():
        print("-", name)

    exit()

mine = mine_lookup[mine_name]

original_name = next(
    name
    for name in MINES.keys()
    if name.lower() == mine_name
)

downtime_hours = random.uniform(10, 70)

blast_delay_days = random.randint(0, 10)

equipment_availability = random.uniform(65, 95)

model = joblib.load(
    "model/production_model.pkl"
)

sample = pd.DataFrame([{

    "reserve_mt":
        mine["reserve_mt"],

    "workforce":
        mine["workforce"],

    "oms":
        mine["oms"],

    "development_m":
        mine["development_m"],

    "rainfall_mm":
        mine["rainfall"],

    "elevation_m":
        mine["elevation"],

    "grade_percent":
        mine["grade"],

    "downtime_hours":
        downtime_hours,

    "blast_delay_days":
        blast_delay_days,

    "equipment_availability":
        equipment_availability

}])

predicted_production = model.predict(sample)[0]

expected_production = mine["annual_production"]

shortfall = (
    expected_production
    - predicted_production
)

issues = []

if equipment_availability < 70:
    issues.append(
        "Critical Equipment Availability"
    )
elif equipment_availability < 80:
    issues.append(
        "Low Equipment Availability"
    )

if downtime_hours > 60:
    issues.append(
        "Excessive Equipment Downtime"
    )
elif downtime_hours > 40:
    issues.append(
        "Elevated Equipment Downtime"
    )

if blast_delay_days > 8:
    issues.append(
        "Severe Blasting Delays"
    )
elif blast_delay_days > 5:
    issues.append(
        "Moderate Blasting Delays"
    )

print("\n====================")
print("Mine:", original_name)

print(
    "Expected Production:",
    round(expected_production)
)

print(
    "Predicted Production:",
    round(predicted_production)
)

print(
    "Estimated Shortfall:",
    round(shortfall)
)

print("\nMajor Contributing Factors:")

if issues:
    for issue in issues:
        print("-", issue)
else:
    print(
        "- No major operational issues detected"
    )

print(
    "\nEquipment Availability:",
    round(equipment_availability, 1),
    "%"
)

print(
    "Downtime Hours:",
    round(downtime_hours, 1)
)

print(
    "Blast Delay Days:",
    blast_delay_days
)

if shortfall > 50000:
    print("Risk Level: HIGH")
elif shortfall > 20000:
    print("Risk Level: MEDIUM")
else:
    print("Risk Level: LOW")