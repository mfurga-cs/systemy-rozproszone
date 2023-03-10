#!/usr/bin/env python3
# W przypadku kiedy klucze API do zewnętrznych serwisów przestaną działać,
# wykonywana jest funkcja generate_mock_data.

from flask import Flask, jsonify, request,render_template
import requests
from datetime import datetime, timedelta
from random import randint

app = Flask(__name__, template_folder=".")

def generate_mock_data(status, date_from, date_to):
  date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
  date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
  delta = date_to - date_from

  result = {
    "status_code": status,
    "data": []
  }

  start = date_from
  for i in range(delta.days + 1):
    result["data"].append({"date": start.strftime("%Y-%m-%d"), "temp": randint(-2, 10)})
    start += timedelta(days=1)

  return result

def fahrenheit_to_celsius(degree):
  return (degree - 32) * (5 / 9)

def get_weatherapi(city: str, date_from: str, date_to: str) -> dict:
  url = "https://api.weatherapi.com/v1/history.json"
  key = "5aec26a4e9644a6994b222841230903"
  params = {
    "key": key,
    "q": city,
    "dt": date_from,
    "end_dt": date_to
  }
  response = requests.get(url, params=params)

  result = {
    "status_code": response.status_code,
    "data": []
  }

  if response.status_code == 200:
    data = response.json()["forecast"]["forecastday"]
    for forecast_day in data:
      date = forecast_day["date"]
      temp = forecast_day["day"]["avgtemp_c"]
      result["data"].append({"date": date, "temp": temp})
  else:
    print(response.text)
    return generate_mock_data(200, date_from, date_to)

  return result

def get_visualcrossing(city: str, date_from: str, date_to: str) -> dict:
  url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date_from}/{date_to}/"
  params = {
    "key": "LZDRZ3VAWUXWX2UEUKZ64VER8",
  }
  response = requests.get(url, params=params)

  result = {
    "status_code": response.status_code,
    "data": []
  }

  if response.status_code == 200:
    data = response.json()["days"]
    for forecast_day in data:
      date = forecast_day["datetime"]
      temp = fahrenheit_to_celsius(forecast_day["temp"])
      result["data"].append({"date": date, "temp": temp})
  else:
    print(response.text)
    return generate_mock_data(200, date_from, date_to)

  return result

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/weather")
def weather():
  city = request.args.get("city")
  date_from = request.args.get("date_from")
  date_to = request.args.get("date_to")

  if city is None or date_from is None or date_to is None:
    return jsonify({"message": "city, date_from, date_to are required"}), 400

  data1 = get_weatherapi(city, date_from, date_to)
  data2 = get_visualcrossing(city, date_from, date_to)

  if data1["status_code"] != 200:
    return jsonify({"message": "Failed to get data from service 1."}), 503

  if data2["status_code"] != 200:
    return jsonify({"message": "Failed to get data from service 2."}), 503

  if len(data1["data"]) != len(data2["data"]):
    return jsonify({"message": "Invalied response from service."}), 503

  response = {
    "average": None,
    "maximum": float("-inf"),
    "minimum": float("+inf"),
    "data": []
  }

  n = len(data2["data"])

  avg = 0
  for i in range(n):
    response["maximum"] = max(response["maximum"],
                              data1["data"][i]["temp"], 
                              data2["data"][i]["temp"])

    response["maximum"] = round(response["maximum"])

    response["minimum"] = min(response["minimum"],
                              data1["data"][i]["temp"], 
                              data2["data"][i]["temp"])

    response["minimum"] = round(response["minimum"])

    temp = (data1["data"][i]["temp"] + data2["data"][i]["temp"]) / 2
    avg += temp
    response["data"].append({
      "date": data2["data"][i]["date"],
      "temp": round(temp)
    })

  avg /= n
  response["average"] = round(avg)
  return jsonify(response)
