import docker

# import docker.errors
# import json
from elasticsearch import Elasticsearch

es = Elasticsearch("http://es01:9200")
from datetime import datetime
import time

running_index = "running_docker_containers"
exited_index = "exited_docker_containers"
others_index = "others_docker_containers"
all_indexes="all_indexes"


def get_connection_to_docker(docker):
    try:
        client = docker.from_env()
        client.ping()
        print("Connected successfully to Docker API!")
        return client
    except docker.errors.DockerException as e:
        print(f"Error connecting to Docker daemon: {e}")
        print("Hint: Is the Docker daemon running? Do you have permission?")
        return None


def get_cpu_percent_with_prev(current_stats, previous_stats):
    try:
        cpu_delta = (
            current_stats["cpu_stats"]["cpu_usage"]["total_usage"]
            - previous_stats["cpu_stats"]["cpu_usage"]["total_usage"]
        )
        system_delta = (
            current_stats["cpu_stats"]["system_cpu_usage"]
            - previous_stats["cpu_stats"]["system_cpu_usage"]
        )

        if system_delta > 0 and cpu_delta > 0:
            online_cpus = (
                len(current_stats["cpu_stats"]["cpu_usage"].get("percpu_usage", []))
                or 1
            )
            return round((cpu_delta / system_delta) * online_cpus * 100.0, 2)
        return 0.0
    except:
        return 0.0


def list_docker_containers(client, time, datetime):
    if not client:
        print("No Docker client available.")
        return [], []

    try:
        containers = client.containers.list(all=True)
    except Exception as e:
        print(f"Failed to list containers: {e}")
        return [], []

    running = []
    exited = []
    other = []

    for container in containers:
        try:
            container.reload()  # Refresh container state
            info = {
                "name": container.name,
                "status": container.status,
                "image": (
                    container.image.tags[0]
                    if container.image.tags
                    else str(container.image.id)[:12]
                ),
                "id": container.short_id,
                "cpu_percent": 0.0,
                "timestamp": datetime.utcnow().isoformat(),
            }

            if container.status == "running":
                try:
                    # stream=False gives one stats sample
                    stats = container.stats(stream=False)
                    time.sleep(1)
                    stats2 = container.stats(stream=False)
                    cpu_percent = get_cpu_percent_with_prev(stats2, stats)
                    info["cpu_percent"] = cpu_percent
                    running.append(info)
                except Exception as e:
                    print(f"Could not get stats for {container.name}: {e}")
                    info["cpu_percent"] = "N/A"
                    running.append(info)
            elif container.status == "exited":
                exited.append(info)
            else:
                other.append(info)

        except Exception as e:
            print(f"Error processing container {container.id}: {e}")

    return exited, running, other


if __name__ == "__main__":
    client = get_connection_to_docker(docker)

    if not client:
        exit(1)

    exited, running, other = list_docker_containers(client, time, datetime)  # type: ignore

    print("\n" + "=" * 60)
    print("EXITED CONTAINERS")
    print("=" * 60)
    if exited:
        for e in exited:
            print(f"Name: {e['name']:<20} | ID: {e['id']} | Image: {e['image']}")
    else:
        print("No exited containers.")

    print("\n" + "=" * 60)
    print("RUNNING CONTAINERS")
    print("=" * 60)
    if running:
        for r in running:
            cpu = r["cpu_percent"]
            cpu_str = f"{cpu:.2f}%" if isinstance(cpu, float) else cpu
            print(
                f"Name: {r['name']:<20} | ID: {r['id']} | CPU: {cpu_str:<8} | Image: {r['image']}"
            )
    else:
        print("No running containers.")

    if other:
        print("\nOther containers (paused, created, etc.):")
        for o in other:
            print(f"  - {o['name']} ({o['status']})")
    try:
        while True:
            print("Docker --> ElasticSearch.")
            exited, running, others = list_docker_containers(client, time, datetime)  # type: ignore
            merge=exited+running+others
            print("Sending all the metrics to elasticsearch....")
            for doc in merge:
                es.index(index=all_indexes,document=doc)
            print("Sending the running metrics to elasticsearch...")
            for doc in running:
                es.index(index=running_index, document=doc)
            print("Sending the exited metrics to elasticsearch...")
            for doc in exited:
                es.index(index=exited_index, document=doc)
            print("Sending the others metrics to elasticsearch....")
            for doc in others:
                es.index(index=others_index, document=doc)
    except Exception as e:
        print(f"There is a problem :{e}.")
    time.sleep(30)
