class SystemConfiguration:
    BROKER_URL = "PLAINTEXT://127.0.0.1:9092"
    SCHEMA_REGISTRY_URL = "http://localhost:8081"
    KSQL_URL = "http://localhost:8088"
    KAFKA_CONNECT_URL = "http://localhost:8083/connectors"
    REST_PROXY_URL = "http://localhost:8082"

class TOPIC_NAMES:
    TRAIN_ARRIVALS_V1 = "com.udacity.trains.arrival.v1"
    TRAIN_TURNSTILE_V1 = "com.udacity.trains.turnstile.v1"
    WEATHER_TEMPERATURE_V1 = "com.udacity.weather.temperature.v1"
    CONNECTOR_NAME = "stations"
    CONNECTOR_TOPIC_PREFIX = "com.connect.transportation."
    CONNECTOR_TOPIC = CONNECTOR_TOPIC_PREFIX + CONNECTOR_NAME

    STATIONS_FAUST_TABLE_V1 = "com.faust.transformed.stations.table.v1"

