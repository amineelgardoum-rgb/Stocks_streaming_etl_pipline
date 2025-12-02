echo "Shutting down the docker compose containers and there volumes!"
if docker compose -p etl -f docker-compose.yml  down -v ;then
	echo "The docker containers are shut down and also there volumes!"
else 
	echo "There is a problem while shutting down the docker containers!">&2
fi
echo "Shutting down the docker container of dbt! "
if docker compose -p etl -f docker-compose.dbt.yml  down -v ;then
	echo "The docker containers are shut down and also there volumes!"
else 
	echo "There is a problem while shutting down the docker containers!">&2
fi
