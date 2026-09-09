import json
import random
import joblib
import pandas as pd

from configur.mines import MINES

COORDINATES = {
    "Balaghat": [21.8089, 80.1834],
    "Chikla": [21.5421, 79.7482],
    "Dongri Buzurg": [21.5312, 79.6825],
    "Mansar": [21.3985, 79.2892],
    "Kandri": [21.4120, 79.2715],
    "Ukwa": [21.9621, 80.4682],
    "Tirodi": [21.6815, 79.7211],
    "Gumgaon": [21.3852, 79.0312],
    "Ramtek (Parseoni)": [21.3961, 79.3284],
    "Sitasaongi": [21.5288, 79.7610],
    "Parsoda": [21.3125, 79.1580],
    "Miragpur": [21.6341, 79.6124],
    "Netra": [21.8512, 80.2415],
    "Beldongri": [21.3251, 79.2841],
    "Gowari Wadhona": [21.4892, 78.9612]
}

model = joblib.load("model/production_model.pkl")

output = []

for mine_name, mine in MINES.items():

    if mine_name not in COORDINATES:
        continue

    downtime = random.uniform(10, 70)
    blast_delay = random.randint(0, 10)
    equipment_availability = random.uniform(65, 95)

    issues = []
    recommendations = []

    if equipment_availability < 70:

        issues.append(
            "Critical Equipment Availability"
        )

        recommendations.append(
            "Increase preventive maintenance"
        )

    elif equipment_availability < 80:

        issues.append(
            "Low Equipment Availability"
        )

        recommendations.append(
            "Improve equipment utilization"
        )

    if downtime > 60:

        issues.append(
            "Excessive Equipment Downtime"
        )

        recommendations.append(
            "Reduce equipment downtime"
        )

    elif downtime > 40:

        issues.append(
            "Elevated Equipment Downtime"
        )

        recommendations.append(
            "Improve maintenance scheduling"
        )

    if blast_delay > 8:

        issues.append(
            "Severe Blasting Delays"
        )

        recommendations.append(
            "Optimize blasting operations"
        )

    elif blast_delay > 5:

        issues.append(
            "Moderate Blasting Delays"
        )

        recommendations.append(
            "Review blasting schedule"
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
            downtime,

        "blast_delay_days":
            blast_delay,

        "equipment_availability":
            equipment_availability

    }])

    predicted = float(
        model.predict(sample)[0]
    )

    expected = float(
        mine["annual_production"]
    )

    shortfall = (
        expected - predicted
    )

    if shortfall > 50000:

        risk = "HIGH"

    elif shortfall > 20000:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    output.append({

        "mine_name":
            mine_name,

        "latitude":
            COORDINATES[mine_name][0],

        "longitude":
            COORDINATES[mine_name][1],

        "expected_production":
            round(expected),

        "predicted_production":
            round(predicted),

        "shortfall":
            round(shortfall),

        "risk":
            risk,

        "equipment_availability":
            round(
                equipment_availability,
                1
            ),

        "downtime_hours":
            round(
                downtime,
                1
            ),

        "blast_delay_days":
            blast_delay,

        "issues":
            issues,

        "recommendations":
            recommendations

    })

with open(
    "mine_data.json",
    "w"
) as f:

    json.dump(
        output,
        f,
        indent=4
    )

print(
    f"mine_data.json created with {len(output)} mines"
)