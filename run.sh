#!/bin/bash

# --- Colors ---
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
BLUE="\e[34m"
RESET="\e[0m"

DAG_ID="minio_to_postgres"


# -------------------------------
# Function: Start a compose file
# -------------------------------
start_compose() {
  local project_name=$1
  local compose_file=$2

  echo -e "${BLUE}Starting Docker Compose project '$project_name' using '$compose_file'...${RESET}"

  if docker compose -p "$project_name" -f "$compose_file" up --build -d --wait; then
    echo -e "${GREEN}✅ '$project_name' started successfully.${RESET}"
  else
    echo -e "${RED}❌ Failed to start '$project_name'!${RESET}" >&2
    exit 1
  fi

  echo
}


# ---------------------------------------
# Function: Wait for Airflow DAG to appear
# ---------------------------------------
wait_for_dag() {
  echo -e "${BLUE}Checking for DAG '$DAG_ID'...${RESET}"

  while true; do
    if docker exec airflow-webserver airflow dags list 2>/dev/null | grep -q "$DAG_ID"; then
      echo -e "${GREEN}✅ DAG '$DAG_ID' found!${RESET}"
      echo -e "${YELLOW}Waiting for Airflow metadata sync...${RESET}"
      sleep 20
      break
    else
      echo -e "${RED}DAG not found, retrying in 10 seconds...${RESET}"
      sleep 10
    fi
  done

  echo
}


# ---------------------------------------
# Function: Trigger and unpause a DAG
# ---------------------------------------
trigger_dag() {
  echo -e "${BLUE}Triggering DAG '$DAG_ID'...${RESET}"

  if docker exec airflow-webserver airflow dags trigger "$DAG_ID"; then
    echo -e "${GREEN}✅ DAG triggered successfully.${RESET}"
  else
    echo -e "${RED}❌ Failed to trigger DAG!${RESET}" >&2
    exit 1
  fi

  echo -e "${YELLOW}Waiting before unpausing DAG...${RESET}"
  sleep 10

  echo -e "${BLUE}Unpausing DAG '$DAG_ID'...${RESET}"
  if docker exec airflow-webserver airflow dags unpause "$DAG_ID"; then
    echo -e "${GREEN}✅ DAG unpaused.${RESET}"
  else
    echo -e "${RED}❌ Failed to unpause DAG.${RESET}"
  fi

  echo
}


# ---------------------------------------
# MAIN RUN SEQUENCE
# ---------------------------------------

# 1) Start main ETL compose
start_compose "etl" "docker-compose.yml"

# 2) Wait for DAG
wait_for_dag

# 3) Trigger + unpause DAG
trigger_dag

# 4) Allow DAG to run and create tables
echo -e "${YELLOW}Waiting 60 seconds for DAG to initialize tables...${RESET}"
sleep 60
echo

# 5) Start DBT compose
start_compose "etl-dbt" "docker-compose.dbt.yml"

# 6) Start Monitor compose
start_compose "etl-monitor" "docker-compose.monitor.yml"

echo -e "${GREEN}` All services are up and the ETL pipeline is running!${RESET}"
