#!/bin/bash

# Colors
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[34m"
YELLOW="\e[33m"
RESET="\e[0m"

DAG_ID="minio_to_postgres"

echo -e "${BLUE}Starting the etl project...${RESET}"
echo -e "${BLUE}run the docker compose...${RESET}"
docker compose -p etl -f docker-compose.yml up --build -d --wait

echo -e "${GREEN}Waiting for DAG '$DAG_ID' to appear in airflow dags list!${RESET}"
while true; do
    if docker exec airflow-webserver airflow dags list 2>/dev/null | grep -q "$DAG_ID"; then
        echo -e "${GREEN}$DAG_ID is found!${RESET}"
        echo -e "${YELLOW}Waiting for the dag to be recognized in the postgres metadata!${RESET}"
        sleep 20
        break
    else
        echo -e "${RED}$DAG_ID is not found, waiting 10 seconds!${RESET}"
        sleep 10
    fi
done

sleep 5
echo -e "${BLUE}Continue...${RESET}"
echo -e "${GREEN}Running the $DAG_ID DAG.${RESET}"

if docker exec airflow-webserver airflow dags trigger "$DAG_ID"; then
    echo -e "${GREEN}The $DAG_ID was triggered successfully!${RESET}"
else
    echo -e "${RED}The $DAG_ID is not triggered successfully!${RESET}" >&2
    exit 1
fi

echo -e "${YELLOW}Waiting to be sure the dag is triggered...${RESET}"
sleep 10

echo -e "${BLUE}Unpause the dag $DAG_ID..!${RESET}"
if docker exec airflow-webserver airflow dags unpause minio_to_postgres; then
    echo -e "${GREEN}The dag is unpaused successfully!${RESET}"
else
    echo -e "${RED}There is a problem${RESET}" 2>/dev/null
fi

echo -e "${YELLOW}Waiting for the dag to successfully create the table in postgres...${RESET}"
sleep 60

echo -e "${BLUE}Run the dbt compose file...${RESET}"
if docker compose -p etl -f docker-compose.dbt.yml up --build -d; then
    echo -e "${GREEN}The dbt container is up${RESET}"
else
    echo -e "${RED}There is a problem${RESET}" 2>/dev/null
    exit 1
fi
echo -e "${GREEN} run the monitor container..."
if ./run_monitor.sh ;then 
	echo -e "${GREEN}the monitor container is up..!${RESET}"
else 
	echo -e "${RED}There is a problem${RESET}" 2>/dev/null
fi
	exit 1
