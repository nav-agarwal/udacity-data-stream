"""Configures KSQL to combine station and turnstile data"""
import json
import logging

import requests

import topic_check


logger = logging.getLogger(__name__)

from constants import SystemConfiguration, TOPIC_NAMES


KSQL_URL = SystemConfiguration.KSQL_URL

KSQL_STATEMENT = """
CREATE TABLE turnstile (line Varchar, station_id Integer, station_name Integer) WITH (KAFKA_TOPIC='{topic_name}', VALUE_FORMAT='avro', key='station_id');

CREATE TABLE turnstile_summary WITH (value_format = 'json') AS SELECT station_id, station_name, COUNT(station_id) as COUNT FROM turnstile GROUP BY station_id, station_name;
""".format(topic_name=TOPIC_NAMES.TRAIN_TURNSTILE_V1)


def execute_statement():
    """Executes the KSQL statement against the KSQL API"""
    if topic_check.topic_exists("TURNSTILE_SUMMARY") is True:
        return

    logging.debug("executing ksql statement...")

    resp = requests.post(
        f"{KSQL_URL}/ksql",
        headers={"Content-Type": "application/vnd.ksql.v1+json"},
        data=json.dumps(
            {
                "ksql": KSQL_STATEMENT,
                "streamsProperties": {"ksql.streams.auto.offset.reset": "earliest"},
            }
        ),
    )

    # Ensure that a 2XX status code was returned
    resp.raise_for_status()


if __name__ == "__main__":
    execute_statement()
