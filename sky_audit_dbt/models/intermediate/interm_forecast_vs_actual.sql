with stg_forecasts as(
    select * from {{ ref('stg_forecasts')}}
),
stg_actuals as(
    select * from {{ ref('stg_actuals')}}
),
stg_cities as(
    select * from {{ ref('stg_cities')}}
),
renamed as(
    select f.city_id as city_id,
        c.city_name as city_name,
        f.target_time as target_time,
        f.forecast_made_at as forecast_made_at,
        f.horizon_hour as horizon_hour,
        f.temperature as forecast_temperature,
        a.temperature as actual_temperature,
        f.precipitation as forecast_precipitation,
        a.precipitation as actual_precipitation,
        f.wind_speed as forecast_wind,
        a.wind_speed as actual_wind,
        round(forecast_temperature - actual_temperature, 1) as temperature_error,
        round(forecast_precipitation - actual_precipitation, 1) as precipitation_error,
        round(forecast_wind - actual_wind, 1) as wind_error
    from stg_forecasts as f
    join stg_actuals a
        on a.city_id = f.city_id
        and f.target_time = a.actual_hour
    join stg_cities as c
        on c.city_id = f.city_id
)
select * from renamed