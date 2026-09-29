CREATE DATABASE IF NOT EXISTS raw;

-- Прогнозы: когда сделан → на какое время
CREATE TABLE raw.forecasts (
    city_id          UInt32,
    forecast_made_at DateTime,
    target_time      DateTime,
    temperature      Float32,
    precipitation    Float32,
    wind_speed       Float32,
    ingested_at      DateTime DEFAULT now()
) ENGINE = MergeTree
ORDER BY (city_id, target_time, forecast_made_at);

-- Факт: какая погода была
CREATE TABLE raw.actuals (
    city_id       UInt32,
    observed_at   DateTime,
    temperature   Float32,
    precipitation Float32,
    wind_speed    Float32,
    ingested_at   DateTime DEFAULT now()
) ENGINE = MergeTree
ORDER BY (city_id, observed_at);

CREATE TABLE raw.cities (
    id        Int32,
    name      String,
    country   String,
    latitude  Decimal(7,4),
    longitude Decimal(7,4)
) ENGINE = PostgreSQL('postgres-app:5432', 'weather', 'cities', 'weather_user', 'weather_password');