import requests

cities = {
    "bratislava": (48.15,17.11),
    "prague": (50.08, 14.43),
    "vienna": (48.21, 16.37)
}

def get_weather(latitude, longtitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longtitude}&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    temps = data["hourly"]["temperature_2m"]
    times = data["hourly"]["time"]

    return temps, times