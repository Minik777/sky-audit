with source as(
	select * from {{ source("raw", "forecasts")}}
),
renamed as (
	select
		city_id,
		forecast_made_at,
		toStartOfHour(forecast_made_at) as forecast_hour,
		target_time,
		dateDiff('hour', forecast_hour, target_time) as horizon_hour,
		temperature,
		precipitation,
		wind_speed,
		ingested_at
	from
		source
	order by forecast_made_at
	limit 1 by city_id, target_time, forecast_hour
	)
	select * from renamed