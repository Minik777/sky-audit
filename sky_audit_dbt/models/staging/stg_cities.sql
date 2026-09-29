with source as(
    select * from {{ source("raw", "cities") }}
        ),
renamed as (
    select
        id as city_id,
        name as city_name,
        country,
        latitude,
        longitude
    from source
)
select * from renamed

