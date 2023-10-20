"""Defines trends calculations for stations"""
import logging

import faust


logger = logging.getLogger(__name__)
from constants import SystemConfiguration, TOPIC_NAMES


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


# Define a Faust Stream that ingests data from the Kafka Connect stations topic and
#   places it into a new topic with only the necessary information.
app = faust.App("stations-stream", broker="kafka://localhost:9092", store="memory://")
# Define the input Kafka Topic. Hint: What topic did Kafka Connect output to?
topic = app.topic(TOPIC_NAMES.CONNECTOR_TOPIC, value_type=Station)
#  Define the output Kafka Topic
out_topic = app.topic(TOPIC_NAMES.STATIONS_FAUST_TABLE_V1, partitions=1)
# Define a Faust Table
table = app.Table(
   TOPIC_NAMES.STATIONS_FAUST_TABLE_V1,
   default=TransformedStation,
   partitions=1,
   changelog_topic=out_topic,
)


#
#
# TODO: Using Faust, transform input `Station` records into `TransformedStation` records. Note that
# "line" is the color of the station. So if the `Station` record has the field `red` set to true,
# then you would set the `line` of the `TransformedStation` record to the string `"red"`
#
#

@app.agent("topic")
async def stationEvent(stationEvents):
     async for event in stationEvents:
        if event.blue:
            line = "blue"
        elif event.green:
            line = "green"
        elif event.red:
            line = "red"
        else:
            line = "unknown"
        
        table[event.station_id] = TransformedStation(
            station_id=event.station_id,
            station_name=event.station_name,
            order=event.order,
            line=line
        )




if __name__ == "__main__":
    app.main()
