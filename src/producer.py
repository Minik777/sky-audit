import requests
from pprint import pprint
import json
import sys
from datetime import datetime
from minio_client import get_json, get_client, BUCKET, ensure_bucket, build_key

from kafka import KafkaProducer
import os

TOPIC_FORECASTS = "topic_forecasts"
TOPIC_ACTUALS = "topic_actuals"

BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVERS", "localhost:9333")
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS,
                         value_serializer=lambda v: v.encode())

def load_to_kafka(payload, topic):
    payload = json.dumps(payload)
    producer.send(topic, value=payload)

def transform_data_for_kafka(fetched_at, data, list_cities):
    hour_start = fetched_at.strftime("%Y-%m-%dT%H:00")
    made_at = fetched_at.strftime("%Y-%m-%dT%H:%M")
    for city, res in zip(list_cities, data):
        city_id = city["id"]
        hourly = res["hourly"]
        now_weather = res["current"]
        current_weather = {
            "city_id": city_id,
            "observed_at": now_weather["time"],
            "temperature": now_weather["temperature_2m"],
            "precipitation": now_weather["precipitation"],
            "wind_speed": now_weather["wind_speed_10m"]
        }
        load_to_kafka(current_weather, TOPIC_ACTUALS)

        for t, temp, prec, wind in zip(hourly["time"],
                                       hourly["temperature_2m"],
                                       hourly["precipitation"],
                                       hourly["wind_speed_10m"]):
            if t < hour_start:
                continue
            row = {
                "city_id": city_id,
                "forecast_made_at": made_at,
                "target_time": t,
                "temperature": temp,
                "precipitation": prec,
                "wind_speed": wind
            }
            load_to_kafka(row, TOPIC_FORECASTS)


def main():
    client = get_client()
    run_dt = datetime.strptime(sys.argv[1], "%Y%m%dT%H%M%S")
    key = build_key(run_dt)
    payload = get_json(client, key, BUCKET)
    fetched_at = datetime.fromisoformat(payload["fetched_at"])
    data =  payload["data"]
    list_cities = payload["list_cities"]
    # if len(list_cities) != len(data):
    #     raise ValueError(f"Ожидали {len(list_cities)} городов, получили {len(data)}")
    print(len(data))
    transform_data_for_kafka(fetched_at, data, list_cities)
    producer.flush()



if __name__ == "__main__":
    main()