#!/bin/bash


shutdown_compose() {
  local project_name=$1
  local compose_file=$2

  echo "Shutting down Docker Compose project '$project_name' using '$compose_file'..."

  if docker compose -p "$project_name" -f "$compose_file" down -v; then
    echo "✅ '$project_name' containers and volumes have been successfully shut down."
  else
    echo "❌ There was a problem shutting down '$project_name' containers!" >&2
  fi

  echo
}

# Shutdown ETL containers
shutdown_compose "etl" "docker-compose.yml"

# Shutdown DBT containers
shutdown_compose "etl-dbt" "docker-compose.dbt.yml"

# Shutdown Monitor containers
shutdown_compose "etl-monitor" "docker-compose.monitor.yml"

echo "All requested Docker Compose projects have been processed."
