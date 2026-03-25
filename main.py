import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from weather_lib import get_weather, cities
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

def create_dataframe(times, temps):
    df = pd.DataFrame({
        "time": times,
        "temperature": temps
    })
    return df

def analyze(df):
    print("Средняя температура: ", df["temperature"].mean())
    print("Максимальная температура: ", df["temperature"].max())
    print("Минимальная температура: ",df["temperature"].min())

def plot_data(df):
    plt.plot(df["time"][::6], df["temperature"][::6])
    plt.xticks(rotation=45)
    plt.title("Temperature over time")
    plt.show()

if __name__ == "__main__":
    city = input("Введите город (bratislava/prague): ")
    lat, lon = cities[city]
    temps, times = get_weather(lat,lon)
    df = create_dataframe(times,temps)
    df.to_csv("weather.csv", index=False)
    analyze(df)
    plot_data(df)
    X = np.arange(len(temps)).reshape(-1,1)
    y = np.array(temps)
    model = LinearRegression()
    model.fit(X, y)
    future = np.array([[len(temps) + i] for i in range(5)])
    predictions = model.predict(future)

    print("Прогноз:", predictions)
