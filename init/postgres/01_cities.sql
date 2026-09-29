CREATE TABLE cities (
    id        SERIAL PRIMARY KEY,
    name      TEXT NOT NULL,
    country   TEXT NOT NULL,
    latitude  NUMERIC(7,4) NOT NULL,
    longitude NUMERIC(7,4) NOT NULL
);

INSERT INTO cities (name, country, latitude, longitude) VALUES
    ('Minsk',      'Belarus', 53.9006,  27.5590),
    ('Moscow',     'Russia',  55.7558,  37.6173),
    ('Warsaw',     'Poland',  52.2297,  21.0122),
    ('Berlin',     'Germany', 52.5200,  13.4050),
    ('Paris',      'France',  48.8566,   2.3522),
    ('London',     'UK',      51.5074,  -0.1278),
    ('Madrid',     'Spain',   40.4168,  -3.7038),
    ('Rome',       'Italy',   41.9028,  12.4964),
    ('Cairo',      'Egypt',   30.0444,  31.2357),
    ('Beijing',    'China',   39.9042, 116.4074),
    ('Tokyo',      'Japan',   35.6762, 139.6503),
    ('Washington', 'USA',     38.9072, -77.0369);