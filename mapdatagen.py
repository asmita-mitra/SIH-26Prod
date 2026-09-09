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

    # -------------------------
    # Simulated Weather
    # -------------------------

    rainfall_mm = random.uniform(0, 120)

    humidity = random.uniform(45, 95)

    temperature = random.uniform(22, 42)

    soil_moisture = min(
        100,
        rainfall_mm * 0.8 + random.uniform(10, 20)
    )

    if rainfall_mm > 80:
        weather = "Heavy Rain"

    elif rainfall_mm > 30:
        weather = "Rain"

    elif humidity > 80:
        weather = "Cloudy"

    else:
        weather = "Clear"

    issues = []
    recommendations = []

    # -------------------------
    # Equipment Availability
    # -------------------------

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

    # -------------------------
    # Downtime
    # -------------------------

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

    # -------------------------
    # Blast Delay
    # -------------------------

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

    # -------------------------
    # Weather Impact
    # -------------------------

    if rainfall_mm > 80:

        issues.append(
            "Heavy Rainfall Affecting Operations"
        )

        recommendations.append(
            "Increase drainage and reduce vehicle movement"
        )

    elif rainfall_mm > 40:

        issues.append(
            "Moderate Rainfall Impacting Efficiency"
        )

        recommendations.append(
            "Adjust shift schedules and monitor haul roads"
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
            rainfall_mm,

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

    weather_impact = 0

    if rainfall_mm > 80:

        weather_impact = 15

    elif rainfall_mm > 40:

        weather_impact = 8

    elif rainfall_mm > 20:

        weather_impact = 4

    adjusted_production = predicted * (
        1 - weather_impact / 100
    )

    expected = float(
        mine["annual_production"]
    )

    shortfall = (
        expected - adjusted_production
    )

    # -------------------------
    # Corrosion Risk
    # -------------------------

    corrosion_score = (
        humidity * 0.6 +
        soil_moisture * 0.4
    )

    if corrosion_score > 80:

        corrosion_risk = "HIGH"

    elif corrosion_score > 60:

        corrosion_risk = "MEDIUM"

    else:

        corrosion_risk = "LOW"

    # -------------------------
    # Weather Analysis
    # -------------------------

    weather_analysis = []

    if rainfall_mm > 80:

        weather_analysis.append(
            "Heavy rainfall is reducing operational hours, slowing transportation and affecting haul-road efficiency."
        )

    elif rainfall_mm > 40:

        weather_analysis.append(
            "Moderate rainfall is causing operational inefficiencies and reduced workforce productivity."
        )

    if soil_moisture > 70:

        weather_analysis.append(
            "High soil moisture is increasing ground instability and slowing excavation activities."
        )

    elif soil_moisture > 50:

        weather_analysis.append(
            "Elevated soil moisture may affect equipment movement and excavation speed."
        )

    if corrosion_risk == "HIGH":

        weather_analysis.append(
            "High humidity and soil moisture increase corrosion risk, potentially causing equipment degradation and downtime."
        )

    elif corrosion_risk == "MEDIUM":

        weather_analysis.append(
            "Environmental conditions indicate moderate corrosion risk for equipment and infrastructure."
        )

    if weather_impact > 0:

        weather_analysis.append(
            f"Estimated production reduced by approximately {weather_impact}% due to current environmental conditions."
        )

    if len(weather_analysis) == 0:

        weather_analysis.append(
            "Current weather conditions are not expected to significantly impact production."
        )

    # -------------------------
    # Risk Level
    # -------------------------

    if shortfall > 50000:

        risk = "HIGH"

    elif shortfall > 20000:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    output.append({

        "mine_name": mine_name,

        "latitude": COORDINATES[mine_name][0],

        "longitude": COORDINATES[mine_name][1],

        "expected_production": round(expected),

        "predicted_production": round(predicted),

        "adjusted_production": round(adjusted_production),

        "shortfall": round(shortfall),

        "risk": risk,

        "weather": weather,

        "temperature": round(temperature, 1),

        "humidity": round(humidity, 1),

        "rainfall_mm": round(rainfall_mm, 1),

        "soil_moisture": round(soil_moisture, 1),

        "weather_impact": weather_impact,

        "corrosion_risk": corrosion_risk,

        "weather_analysis": weather_analysis,

        "equipment_availability": round(
            equipment_availability,
            1
        ),

        "downtime_hours": round(
            downtime,
            1
        ),

        "blast_delay_days": blast_delay,

        "issues": issues,

        "recommendations": recommendations

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