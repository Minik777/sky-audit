import os

from kafka import KafkaConsumer
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVERS", "localhost:9333")
CLICKHOUSE_URL = os.getenv("CLICKHOUSE_URL", "http://localhost:8333")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.environ["CLICKHOUSE_PASSWORD"]

TOPIC_FORECASTS = "topic_forecasts"
TOPIC_ACTUALS = "topic_actuals"

TABLES  = {
    TOPIC_FORECASTS: "raw.forecasts",
    TOPIC_ACTUALS: "raw.actuals",
}

AUTH = (CLICKHOUSE_USER, CLICKHOUSE_PASSWORD)

# def execute(query: str) -> str:
#     response = requests.post(CLICKHOUSE_URL, params={"query": query}, auth=AUTH)
#     response.raise_for_status()
#     return response.text
#
# def parse_messages(message):
#     # Здесь эта функция будет ненужна, так как для clickhouse нужны строки формата json
#     # и нет нужды превщащать их в объекты словаря
#     return json.loads(message)

def load_to_clickhouse(table, rows):
    query = f"INSERT INTO {table} FORMAT JSONEachRow"
    rows_like_str = "\n".join(rows)
    response = requests.post(CLICKHOUSE_URL,
                             params={"query": query, "date_time_input_format": "best_effort"},
                             auth=AUTH,
                             data=rows_like_str.encode("utf-8"),
                             )
    response.raise_for_status()

def main():
    consumer = KafkaConsumer(
        TOPIC_FORECASTS,
        TOPIC_ACTUALS,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id="sky_audit_clickhouse_loader",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
    )
    print("Consumer started")

    while True:
        batch = consumer.poll(timeout_ms=5000)
        if not batch:
            continue
        # pprint(type(batch), width=120, compact=True)

        # здесь tp это объект класса TopicPartition, там внутри и топик и партиция,
        # а messages это 500 сообщений за раз из одного топика,\
        # Кафка по дефолту за один poll больше не может взять
        for tp, messages in batch.items():
            table = TABLES[tp.topic]
            rows = [msg.value.decode("utf-8") for msg in messages]
            # print(type(rows))
            load_to_clickhouse(table, rows)
        consumer.commit()



if __name__ == "__main__":
    main()
