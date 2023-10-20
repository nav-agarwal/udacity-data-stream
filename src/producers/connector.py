"""Configures a Kafka Connector for Postgres Station data"""
import json
import logging

import requests

logger = logging.getLogger(__name__)

from constants import SystemConfiguration, TOPIC_NAMES


def configure_connector():
    """Starts and configures the Kafka Connect connector"""
    logging.debug("creating or updating kafka connect connector...")

    resp = requests.get(f"{SystemConfiguration.KAFKA_CONNECT_URL}/{TOPIC_NAMES.CONNECTOR_NAME}")
    if resp.status_code == 200:
        logging.debug("connector already created skipping recreation")
        return

    # TODO: Complete the Kafka Connect Config below.
    # Directions: Use the JDBC Source Connector to connect to Postgres. Load the `stations` table
    # using incrementing mode, with `stop_id` as the incrementing column name.
    # Make sure to think about what an appropriate topic prefix would be, and how frequently Kafka
    # Connect should run this connector (hint: not very often!)
        return
    config = {
        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
        "key.converter": "org.apache.kafka.connect.json.JsonConverter",
        "key.converter.schemas.enable": "false",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter.schemas.enable": "false",
        "topic.prefix": TOPIC_NAMES.CONNECTOR_TOPIC_PREFIX,
        "connection.url": "jdbc:postgresql://postgres:5432/cta",
        "connection.user": "cta_admin",
        "connection.password": "chicago",
        "batch.max.rows": "500",
        "table.whitelist": "stations",
        "poll.interval.ms": "8640000",  # Poll every 5 seconds
        "mode": "incrementing",
        "incrementing.column.name": "stop_id",
    }
    
    logger.info("connector code not completed skipping connector creation")
    resp = requests.post(
        SystemConfiguration.KAFKA_CONNECT_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "name": TOPIC_NAMES.CONNECTOR_NAME,
            "config": config
        }),
    )

    ## Ensure a healthy response was given
    resp.raise_for_status()
    logging.debug("connector created successfully")

if __name__ == "__main__":
    configure_connector()
