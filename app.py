from flask import Flask, request, jsonify
from weather_lib import get_weather, cities
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return "Server works"


@app.route("/weather")
def weather():
    city = request.args.get("city") 

    if not city:
        return jsonify({"error": "City not found"})

    if city not in cities:
        return jsonify({"error": "City not found"})
    
    lat, lon = cities[city]
    temps, times = get_weather(lat, lon)

    X = np.arange(len(temps)).reshape(-1,1)
    y = np.arange(len(temps))

    model = LinearRegression()
    model.fit(X,y)

    future = np.array([[len(temps) + i] for i in range(5)])
    prediction = model.predict(future)

    df = pd.DataFrame({
        "time": times,
        "temperature": temps
    })

    avg_temp = df["temperature"].mean()
    max_temp = df["temperature"].max()
    min_temp = df["temperature"].min()

    hours = request.args.get("hours")
    try:
        hours = int(hours)
    except:
        hours = 5

    temps_cut = temps[:hours]
    times_cut = times[:hours]

    df = pd.DataFrame({
        "temperature": temps_cut,
        "time": times_cut
    })

    return jsonify({
        "city": city,
        "temperature": temps_cut,
        "time": times_cut,
        "avg_temp": avg_temp,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "prediction": prediction.tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)