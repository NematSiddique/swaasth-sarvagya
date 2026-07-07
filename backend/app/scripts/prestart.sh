#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/backend_pre_start.py

# Run Flyway migrations here
# (This is where you would add your Flyway command)

# Create initial data in DB
python app/initial_data.py
