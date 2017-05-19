#!/usr/bin/env bash

RUN_FOR=300
RADAR_COM_PORT="/dev/ttyUSB0"
RADAR_LANE=4
RADAR_LAT="29.6216931"
RADAR_LON="-82.3867591"
DSRC_IP_ADDRESS="169.254.30.4"
DSRC_REMOTE_PORT=4200
ASSOCIATION_THRESHOLD=150
OUTPUT_PORT=24601

python main.py --run-for $RUN_FOR --radar-lane $RADAR_LANE --dsrc-ip-address $DSRC_IP_ADDRESS --dsrc-remote-port $DSRC_REMOTE_PORT --association-threshold $ASSOCIATION_THRESHOLD --output-port $OUTPUT_PORT --v --record-csv