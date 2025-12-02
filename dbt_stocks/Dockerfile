# Use the official dbt-postgres image
FROM ghcr.io/dbt-labs/dbt-postgres:1.8.latest

# Set working directory
WORKDIR /usr/app

# Copy your dbt project into the container
COPY . /usr/app

# Ensure dbt is executable
RUN dbt --version
