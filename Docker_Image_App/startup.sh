#!/usr/bin/env bash
./docker-entrypoint.sh postgres &
sleep 8
python3 ./ccmgmt_data/app.py