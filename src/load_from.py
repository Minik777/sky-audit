import requests
from connect_to_pg import make_list_cities
from pprint import pprint
import sys
import json
from minio_client import get_client, ensure_bucket, put_json, build_key, BUCKET
from datetime import datetime, timezone

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def make_params():
    list_cities = make_list_cities()
    list_lat = ",".join(str(city["latitude"]) for city in list_cities)
    list_lon = ",".join(str(city["longitude"]) for city in list_cities)

    dict_params = {
        "latitude": list_lat,
        "longitude": list_lon,
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "current": "temperature_2m,precipitation,wind_speed_10m",
        "forecast_days": "7",
        "timezone": "UTC"
    }
    return dict_params, list_cities

def get_from_web(params):
    response = requests.get(OPEN_METEO_URL,
                            params=params
                            )
    response.raise_for_status()
    return response.json()

def main():
    params, list_cities = make_params()
    data = get_from_web(params)
    run_dt = datetime.strptime(sys.argv[1], "%Y%m%dT%H%M%S")
    key = build_key(run_dt)
    fetched_at = datetime.now(timezone.utc)
    time_dt_data_cities = {"fetched_at": fetched_at.isoformat(), "data": data, "list_cities": list_cities}
    client = get_client()
    print(data)
    if len(list_cities) != len(data):
        raise ValueError(f"Ожидали {len(list_cities)} городов, получили {len(data)}")
    print(len(data))
    ensure_bucket(client, BUCKET)
    put_json(client, key, time_dt_data_cities, BUCKET)

    # transform_data_for_clickhouse(data, list_cities)
    # producer.flush()



if __name__ == "__main__":
    main()