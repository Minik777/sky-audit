import os
import psycopg2
from pprint import pprint
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5333")
PG_USER = os.getenv("APP_POSTGRES_USER")
PG_PASSWORD = os.getenv("APP_POSTGRES_PASSWORD")
PG_DB = os.getenv("APP_POSTGRES_DB")

connection = psycopg2.connect(user=PG_USER,
                              password=PG_PASSWORD,
                              host=PG_HOST,
                              port=PG_PORT,
                              database=PG_DB)

def get_cities():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM cities")
        cities = cursor.fetchall()
        return cities

def make_list_cities():
    cities = get_cities()
    list_cities = []
    for city in cities:
        dict_city = {
            "id": city[0],
            "name": city[1],
            "country": city[2],
            "latitude": float(city[3]),
            "longitude": float(city[4])
        }
        list_cities.append(dict_city)
    return list_cities

def main():
    list_cities = make_list_cities()
    pprint(list_cities)

if __name__ == "__main__":
    main()




