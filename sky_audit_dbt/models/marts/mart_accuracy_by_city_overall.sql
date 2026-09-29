with interm_forecast_vs_actual as(
    select * from {{ ref('interm_forecast_vs_actual')}}
),
aggregated as(
    select
        city_id,
        city_name,
        count(horizon_hour) as n_comparisons,
        round(avg(abs(temperature_error)), 2) as mae_temperature_error,
        round(avg(abs(precipitation_error)), 2) as mae_precipitation_error,
        round(avg(abs(wind_error)), 2) as mae_wind_error,
        round(avg(temperature_error), 2) as bias_temperature_error,
        round(avg(precipitation_error), 2) as bias_precipitation_error,
        round(avg(wind_error), 2) as bias_wind_error
    from interm_forecast_vs_actual
    group by city_id, city_name
    order by city_id, city_name
)
select * from aggregated