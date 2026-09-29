with source as(
    select * from {{ source("raw", "actuals") }}
    ),
renamed as(
    select
        city_id,
        observed_at,
        toStartOfHour(observed_at + interval 30 MINUTE) as actual_hour,
        temperature,
        precipitation,
        wind_speed,
        ingested_at
    from
        source
    order by
        city_id, abs(dateDiff('minute', observed_at, actual_hour))
    limit 1 by city_id, actual_hour
)
select * from renamed