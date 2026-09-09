import requests

API_KEY = "6587b7b66bac9ddaca2749bc5ad30967"


def get_weather(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}"
        f"&lon={lon}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    try:

        response = requests.get(url, timeout=10)

        data = response.json()

        print("API Response:")
        print(data)

        if "main" not in data:
            return {
                "error": data.get("message", "Unknown API error")
            }

        rainfall = 0

        if "rain" in data:
            rainfall = data["rain"].get("1h", 0)

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["main"],
            "rainfall_mm": rainfall
        }

    except Exception as e:

        return {
            "error": str(e)
        }


weather = get_weather(
    21.8089,
    80.1834
)

print("\nProcessed Weather:")
print(weather)