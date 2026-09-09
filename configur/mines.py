import pandas as pd

from configur.utils import midpoint

MINES = {}

df = pd.read_csv("data/moil_mines_data.csv")

for _, row in df.iterrows():

    mine_name = row["Mine Name"]

    monthly_prod = midpoint(
        row["Monthly Production (MT)"]
    )

    MINES[mine_name] = {

        "reserve_mt":
            midpoint(row["Reserve (MT)"]),

        "workforce":
            midpoint(row["Workforce"]),

        "oms":
            midpoint(row["OMS (Tonnes)"]),

        "development_m":
            midpoint(
                row["Monthly Development (m)"]
            ),

        "annual_production":
            monthly_prod * 12,

        "rainfall":
            midpoint(
                row["Rainfall (mm/yr)"]
            ),

        "elevation":
            midpoint(
                row["Elevation (m)"]
            ),

        "grade":
            midpoint(
                row["Grade (% Mn)"]
            ),

        "mine_type":
            row["Mine Type"]

    }

MINES["Balaghat"] = {
    "reserve_mt": 24.75,
    "workforce": 1420,
    "oms": 0.84,
    "development_m": 1859,
    "annual_production": 263170,
    "rainfall": 1500,
    "elevation": 600,
    "grade": 45,
    "mine_type": "Underground"
}

MINES["Chikla"] = {
    "reserve_mt": 7.14,
    "workforce": 1420,
    "oms": 0.838,
    "development_m": 1387,
    "annual_production": 176786,
    "rainfall": 1150,
    "elevation": 325,
    "grade": 42,
    "mine_type": "Underground"
}

MINES["Dongri Buzurg"] = {
    "reserve_mt": 23.58,
    "workforce": 1100,
    "oms": 0.90,
    "development_m": 1200,
    "annual_production": 200000,
    "rainfall": 1150,
    "elevation": 325,
    "grade": 46,
    "mine_type": "Open Cast"
}