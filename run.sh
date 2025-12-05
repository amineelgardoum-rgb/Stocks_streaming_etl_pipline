#!/bin/bash

# =====================================
# Colors
# =====================================
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[34m"
YELLOW="\e[33m"
RESET="\e[0m"

# =====================================
# Global Vars
# =====================================
PROJECT_NAME="etl"
DAG_ID="minio_to_postgres"

# =====================================
# Function: wait_for_elasticsearch
# =====================================
wait_for_elasticsearch() {
    echo -e "${BLUE}Checking if Elasticsearch is running...${RESET}"

    TIMEOUT=120
    ELAPSED=0
    INTERVAL=5

    while true; do
        if curl -s http://localhost:9200 >/dev/null; then
            echo -e "${GREEN}Elasticsearch is running!${RESET}"
            return 0
        else
            echo -e "${YELLOW}Elasticsearch not up yet. Waiting ${INTERVAL}s...${RESET}"
            sleep $INTERVAL
            ELAPSED=$((ELAPSED + INTERVAL))

            if [ $ELAPSED -ge $TIMEOUT ]; then
                echo -e "${RED}Timeout reached! Elasticsearch did not start.${RESET}" >&2
                return 1
            fi
        fi
    done
}

# =====================================
# STEP 1 — RUN MAIN ETL SERVICES
# =====================================
echo -e "${BLUE}Starting main ETL stack...${RESET}"
docker compose -p $PROJECT_NAME -f docker-compose.yml up --build -d --wait || {
    echo -e "${RED}Failed to start ETL compose!${RESET}"
    exit 1
}

# =====================================
# STEP 2 — WAIT FOR AIRFLOW DAG
# =====================================
echo -e "${GREEN}Waiting for DAG '$DAG_ID' to appear...${RESET}"

while true; do
    if docker exec airflow-webserver airflow dags list 2>/dev/null | grep -q "$DAG_ID"; then
        echo -e "${GREEN}✔ DAG $DAG_ID FOUND!${RESET}"
        sleep 20
        break
    else
        echo -e "${YELLOW}⏳ DAG not found, retrying...${RESET}"
        sleep 10
    fi
done

# =====================================
# STEP 3 — TRIGGER THE DAG
# =====================================
echo -e "${BLUE}Triggering Airflow DAG...${RESET}"

if docker exec airflow-webserver airflow dags trigger "$DAG_ID"; then
    echo -e "${GREEN}✔ DAG Triggered successfully!${RESET}"
else
    echo -e "${RED}❌ Failed to trigger DAG${RESET}"
    exit 1
fi

sleep 10

echo -e "${BLUE}Unpausing DAG...${RESET}"
docker exec airflow-webserver airflow dags unpause "$DAG_ID"

echo -e "${YELLOW}Waiting for Postgres tables creation...${RESET}"
sleep 60

# =====================================
# STEP 4 — RUN DBT SERVICES
# =====================================
echo -e "${BLUE}Starting DBT container...${RESET}"
docker compose -p $PROJECT_NAME -f docker-compose.dbt.yml up --build -d || {
    echo -e "${RED}❌ Failed to start DBT container${RESET}"
    exit 1
}
echo -e "${GREEN}✔ DBT container is UP${RESET}"

# =====================================
# STEP 5 — WAIT FOR ELASTICSEARCH, THEN START MONITOR
# =====================================
if wait_for_elasticsearch; then
    echo -e "${BLUE}Starting monitor container...${RESET}"
    docker compose -p $PROJECT_NAME -f docker-compose.monitor.yml up --build -d || {
        echo -e "${RED}❌ Monitor container failed${RESET}"
        exit 1
    }
    echo -e "${GREEN}✔ Monitor container is UP${RESET}"
else
    exit 1
fi

# =====================================
# STEP 6 — START API CONTAINER
# =====================================
echo -e "${BLUE}Starting API container...${RESET}"
docker compose -p $PROJECT_NAME -f docker-compose.api.yml up --build -d || {
    echo -e "${RED}❌ API container failed${RESET}"
    exit 1
}

echo -e "${GREEN} ALL SERVICES STARTED SUCCESSFULLY!${RESET}"
