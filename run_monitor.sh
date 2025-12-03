#!/bin/bash

# ==========================
# monitor.sh
# Wait for Elasticsearch and start monitor container
# ==========================

# Colors
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[34m"
YELLOW="\e[33m"
RESET="\e[0m"

MONITOR_COMPOSE="docker-compose.monitor.yml"
PROJECT_NAME="etl"

echo -e "${BLUE}Checking if Elasticsearch is running...${RESET}"

# Timeout after 2 minutes (120s)
TIMEOUT=120
ELAPSED=0
INTERVAL=5

while true; do
    if curl -s http://localhost:9200 >/dev/null; then
        echo -e "${GREEN}Elasticsearch is running!${RESET}"
        echo -e "${BLUE}Starting monitor container...${RESET}"
        docker compose -p $PROJECT_NAME -f $MONITOR_COMPOSE up --build -d
        echo -e "${GREEN}Monitor container started successfully.${RESET}"
        break
    else
        echo -e "${YELLOW}Elasticsearch not up yet. Waiting ${INTERVAL}s...${RESET}"
        sleep $INTERVAL
        ELAPSED=$((ELAPSED + INTERVAL))

        if [ $ELAPSED -ge $TIMEOUT ]; then
            echo -e "${RED}Timeout reached! Elasticsearch did not start.${RESET}" >&2
            exit 1
        fi
    fi
done
