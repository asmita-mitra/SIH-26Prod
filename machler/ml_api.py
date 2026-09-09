from fastapi import FastAPI
import pandas as pd
import joblib

from configur.mines import MINES

app = FastAPI()

model = joblib.load("production_model.pkl")


@app.post("/forecast")
def forecast(data: dict):

    mine_name = data["mine_name"]

    if mine_name not in MINES:
        return {"error": "Mine not found"}

    mine = MINES[mine_name]

    sample = pd.DataFrame([{
        "reserve_mt": mine["reserve_mt"],
        "workforce": mine["workforce"],
        "oms": mine["oms"],
        "development_m": mine["development_m"],
        "downtime_hours": mine["downtime_hours"],
        "blast_delay_days": mine["blast_delay_days"],
        "equipment_availability": mine["equipment_availability"]
    }])

    predicted_production = float(
        model.predict(sample)[0]
    )

    expected_production = mine["annual_production"]

    shortfall = expected_production - predicted_production

    issues = []

    if mine["equipment_availability"] < 70:
        issues.append({
            "factor": "equipment_availability",
            "impact": "HIGH"
        })

    elif mine["equipment_availability"] < 80:
        issues.append({
            "factor": "equipment_availability",
            "impact": "MEDIUM"
        })

    if mine["downtime_hours"] > 60:
        issues.append({
            "factor": "downtime_hours",
            "impact": "HIGH"
        })

    elif mine["downtime_hours"] > 40:
        issues.append({
            "factor": "downtime_hours",
            "impact": "MEDIUM"
        })

    if mine["blast_delay_days"] > 5:
        issues.append({
            "factor": "blast_delay_days",
            "impact": "MEDIUM"
        })

    if shortfall > 50000:
        risk = "HIGH"
    elif shortfall > 20000:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "predicted_production_mt": round(predicted_production, 2),
        "expected_production_mt": round(expected_production, 2),
        "estimated_shortfall_mt": round(shortfall, 2),
        "shortfall_risk_level": risk,
        "contributing_factors": issues
    }