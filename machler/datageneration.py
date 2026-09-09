import pandas as pd
import random

from configur.mines import MINES

data = []

for mine_name, mine in MINES.items():

    for i in range(1000):

        downtime = random.uniform(0, 80)

        blast_delay = random.randint(0, 10)

        equipment_availability = random.uniform(60, 100)

        production_factor = (
            equipment_availability / 100
        )

        production_factor *= (
            1 - downtime / 500
        )

        production_factor *= (
            1 - blast_delay / 50
        )

        predicted_production = (
            mine["annual_production"]
            * production_factor
        )

        shortfall = (
            mine["annual_production"]
            - predicted_production
        )

        data.append({

            "mine_name": mine_name,

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
                equipment_availability,

            "predicted_production_mt":
                predicted_production,

            "shortfall_mt":
                shortfall

        })

df = pd.DataFrame(data)

df.to_csv(
    "data/production_prediction_dataset.csv",
    index=False
)

print("Dataset created!")
print("Rows:", len(df))
print("Mines:", len(MINES))