\# 📈 Real-Time Financial Market Data Pipeline

## 🌟 Project Overview

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-232F3E?style=for-the-badge&logo=apachekafka&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-0172E3?style=for-the-badge&logo=apacheairflow&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF6945?style=for-the-badge&logo=dbt&logoColor=white)

This project implements a **production-grade, event-driven data pipeline** that ingests, processes, and transforms real-time financial market data from **Finnhub** into actionable analytics. The architecture follows modern data engineering best practices with a clear separation of concerns across extraction, streaming, storage, and transformation layers.

**Key Technical Highlights:**

* **Event-Driven Architecture** using Apache Kafka for real-time data streaming and decoupling
* **Medallion Architecture** (Bronze/Silver/Gold layers) for progressive data refinement
* **Orchestrated ELT workflows** with Apache Airflow for reliable, scheduled transformations
* **Analytics-ready data models** built with dbt for business intelligence and downstream consumption

---

## 🏗️ Architecture Overview

The pipeline consists of four primary layers, each handling a specific stage of the data journey:

### 1️⃣ **Extract Layer** (Data Ingestion)

**Components:** Finnhub API → Kafka Producer

The pipeline begins with the **Kafka Producer** service, which continuously fetches real-time stock market data from the **Finnhub API**. This includes:

- Real-time stock prices
- Trading volumes
- Market metadata

The producer formats and publishes this data to Kafka topics, creating a continuous stream of financial events.

---

### 2️⃣ **Streaming Layer** (Message Broker)

**Components:** Kafka Cluster (Producer, Broker, Consumer)

At the heart of the architecture sits **Apache Kafka**, providing:

- **High-throughput message streaming** with distributed partitions
- **Fault tolerance** through replication across brokers
- **Decoupling** between data producers and consumers
- **Backpressure handling** allowing consumers to process at their own pace

The Kafka cluster consists of:

- **Kafka Producer**: Publishes financial events to topics
- **Kafka Broker**: Manages topic partitions and message persistence
- **Kafka Consumer**: Subscribes to topics and delivers data to downstream storage

This architecture ensures that even if downstream systems are temporarily unavailable, no data is lost—messages remain in Kafka until successfully processed.

---

### 3️⃣ **Transform and Load Layer** (ELT Processing)

**Components:** Airflow (Orchestration) → MinIO (Data Lake) → PostgreSQL (Data Warehouse) → dbt (Transformation)

This layer handles the core ELT (Extract, Load, Transform) workflow:

#### **a) Data Lake Storage (Bronze Layer)**

The **Kafka Consumer** reads messages from Kafka topics and writes raw data to **MinIO**, an S3-compatible object storage serving as the Bronze layer. This creates an immutable, historical record of all ingested data.

#### **b) Orchestration**

**Apache Airflow** orchestrates the entire ELT process through scheduled DAGs:

- Monitors MinIO for new data files
- Triggers data loading into the warehouse
- Manages dbt transformation jobs
- Handles retries and failure recovery

#### **c) Data Warehouse (Silver & Gold Layers)**

Data flows from MinIO into **PostgreSQL** (labeled as the Data Warehouse in the architecture), where:

- **Silver Layer**: Cleaned and standardized data with basic transformations
- **Gold Layer**: Business-ready aggregated metrics and analytical models

#### **d) Transformation with dbt**

**dbt (data build tool)** manages all SQL-based transformations:

- Defines modular, version-controlled data models
- Implements data quality tests
- Documents data lineage
- Builds the Silver and Gold layer tables incrementally

---

### 4️⃣ **Consumption Layer** (Analytics & APIs)

**Components:** RESTful API (with green lightning bolt icon)

The final layer exposes transformed data for consumption:

- **RESTful API** provides programmatic access to analytics-ready datasets
- Supports integration with BI tools, dashboards, and downstream applications
- Serves real-time and historical financial metrics from the Gold layer

---

## 🛠️ Technology Stack

<<<<<<< HEAD
| Layer                    | Technology     | Purpose                                    |
| ------------------------ | -------------- | ------------------------------------------ |
| **Data Source**    | Finnhub API    | Real-time financial market data provider   |
| **Streaming**      | Apache Kafka   | Distributed event streaming platform       |
| **Object Storage** | MinIO          | S3-compatible data lake (Bronze layer)     |
| **Orchestration**  | Apache Airflow | Workflow automation and scheduling         |
| **Data Warehouse** | PostgreSQL     | Relational database for Silver/Gold layers |
| **Transformation** | dbt            | SQL-based data modeling and testing        |
| **API Layer**      | RESTful API    | Data consumption interface                 |
=======
This pipeline was built using a best-in-class modern data stack, emphasizing performance, scalability, and ease of maintenance.

| Category                    | Tool / Service                                                                                                                                                                                                             | Technical Functionality and Rationale                                                                                                                                |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data Ingestion**    | ![\w](https://img.shields.io/badge/Finnhub-000000?style=for-the-badge&logo=finnhub&logoColor=white)                                                                                                                          | Primary source for streaming real-time stock market data.                                                                                                            |
| **Streaming Layer**   | ![\w](https://img.shields.io/badge/Kafka-232F3E?style=for-the-badge&logo=apachekafka&logoColor=white)&nbsp;&nbsp;![\w](https://img.shields.io/badge/Zookeeper-232F3E?style=for-the-badge&logo=apachezookeeper&logoColor=white) | Provides a distributed commit log for high-throughput, fault-tolerant message delivery, decoupling producers from consumers. Zookeeper handles cluster coordination. |
| **Data Lake Staging** | ![\w](https://img.shields.io/badge/MinIO-FF0000?style=for-the-badge&logo=minio&logoColor=white)                                                                                                                              | Serves as the immutable Bronze Layer (RAW DATA) for historical storage, ensuring data is never lost.                                                                 |
| **Orchestration**     | ![\w](https://img.shields.io/badge/Airflow-0172E3?style=for-the-badge&logo=apacheairflow&logoColor=white)                                                                                                                    | Manages complex DAGs (Directed Acyclic Graphs) for scheduling, monitoring, and idempotently retrying ELT jobs.                                                       |
| **Transformation**    | ![\w](https://img.shields.io/badge/dbt-FF6945?style=for-the-badge&logo=dbt&logoColor=white)                                                                                                                                  | Defines data models using modular, reusable SQL transformations to build the Silver and Gold layers, providing robust testing and documentation.                     |
| **Data Warehouse**    | ![\w](https://img.shields.io/badge/Postgres-22B4E8?style=for-the-badge&logo=snowflake&logoColor=white)                                                                                                                      | Cloud-native, scalable Data Warehouse used for final storage, complex querying, and providing the compute layer for dbt transformations.                             |
| **Monitoring**        | ![\w](https://img.shields.io/badge/Kafdrop-007ACC?style=for-the-badge&logoColor=white)                                                                                                                                       | Web UI for real-time inspection of Kafka topic partitions and message consumption offsets.                                                                           |
>>>>>>> 892ea5c823d4aeecdbce5fd27b81d710324100db

---

## 📊 Data Flow Journey

1. **Ingestion**: Finnhub API delivers real-time market data to the Kafka Producer
2. **Streaming**: Producer publishes events to Kafka topics, where they're persisted across broker nodes
3. **Raw Storage**: Consumer reads from Kafka and writes raw JSON/CSV files to MinIO (Bronze layer)
4. **Orchestration**: Airflow triggers scheduled DAGs to process new data
5. **Loading**: Data is copied from MinIO into PostgreSQL staging tables
6. **Transformation**: dbt runs SQL models to create cleaned (Silver) and aggregated (Gold) datasets
7. **Serving**: RESTful API exposes transformed data for analytics and reporting

---

## 🔑 Key Architectural Decisions

### **Why Kafka?**

- Handles millions of events per second with horizontal scalability
- Provides guaranteed message delivery and ordering
- Decouples data ingestion from processing, preventing cascading failures

### **Why Medallion Architecture?**

- **Bronze (Raw)**: Immutable source of truth for data recovery and auditing
- **Silver (Cleaned)**: Standardized data ready for analytics
- **Gold (Aggregated)**: Pre-computed business metrics for fast querying

### **Why Airflow + dbt?**

- Airflow manages infrastructure tasks (file transfers, scheduling)
- dbt focuses on SQL transformations with built-in testing and documentation
- Clear separation of concerns improves maintainability

### **Why PostgreSQL?**

Based on the architecture diagram, this implementation uses PostgreSQL as the data warehouse, which provides:

- Cost-effective solution for moderate data volumes
- Full SQL compliance for complex analytics
- Easy integration with dbt and other open-source tools

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Finnhub API key
- PostgreSQL credentials

### Quick Start

```bash
# Clone the repository
git clone https://github.com/amineelgardoum-rgb/Stocks_streaming_etl_pipline.git
cd Stocks_streaming_etl_pipline

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Start all services
./run.sh
# Or manually: docker-compose up -d

# Access UIs
# Airflow: http://localhost:8080 (admin/admin)
# Kafdrop: http://localhost:9000
# MinIO: http://localhost:9001
```

### Running the Pipeline

1. **Verify Kafka is streaming**: Check Kafdrop UI for active topics and messages
2. **Configure Airflow connections**: Add PostgreSQL, MinIO, and Finnhub credentials
3. **Trigger the DAG**: Enable `minio_to_snowflake` DAG in Airflow UI (note: despite the name, this loads to PostgreSQL)
4. **Monitor execution**: Watch task progress in Airflow and data flow in Kafdrop
5. **Query results**: Connect to PostgreSQL and query Gold layer tables

---

## 📁 Project Structure

```
Stocks_streaming_etl_pipline/
├── api/                          # RESTful API service
│   ├── routers/                 # API route handlers
│   ├── utils/                   # Helper utilities
│   ├── api.py                   # Main FastAPI application
│   ├── Dockerfile               # API container build
│   └── requirements.txt         # API dependencies
├── producer/                     # Kafka producer service
│   ├── producer.py              # Main entry point
│   ├── fetch_job.py             # Finnhub API integration
│   ├── produce_messages.py      # Kafka publishing logic
│   ├── Dockerfile               # Producer container build
│   └── requirements.txt         # Producer dependencies
├── consumer/                     # Kafka consumer service
│   ├── consumer.py              # Main entry point
│   ├── consume_messages.py      # Kafka consumption logic
│   ├── s3_init.py               # MinIO integration
│   ├── Dockerfile               # Consumer container build
│   └── requirements.txt         # Consumer dependencies
├── dags/                         # Airflow DAGs
│   ├── minio_to_postgres.py    # Main ELT orchestration
|  
├── dbt_stocks/                   # dbt transformation project
│   ├── models/
│   │   ├── bronze/              # Raw data models
│   │   ├── silver/              # Cleaned data models
│   │   └── gold/                # Analytics models
│   ├── tests/                   # Data quality tests
│   └── dbt_project.yml          # dbt configuration
├── docker_monitor/               # Container monitoring tools
├── config/                       # Centralized configuration
├── assets/                       # Documentation assets
│   ├── stocks_pipeline.jpg      # Architecture diagram
│   ├── data_warehouse.jpg       # Warehouse schema
│   └── archi.svg                # Editable architecture
├── logs/                         # Application logs
├── plugins/                      # Airflow custom plugins
├── venv/                         # Python virtual environment
├── docker-compose.yml            # Main service orchestration
├── docker-compose.api.yml        # API service config
├── docker-compose.dbt.yml        # dbt service config
├── docker-compose.monitor.yml    # Monitoring service config
├── run.sh                        # Startup script
├── down.sh                       # Teardown script   
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## 🔮 Future Enhancements

- **Real-time Dashboards**: Integrate Streamlit or Apache Superset for live visualization
- **Data Quality Monitoring**: Implement Great Expectations for automated data validation
- **Infrastructure as Code**: Add Terraform modules for cloud deployment
- **Machine Learning Integration**: Build predictive models on Gold layer data
- **Multi-region Deployment**: Expand to global Kafka clusters for reduced latency
- **Change Data Capture**: Add CDC capabilities for incremental processing

---

## 📝 Additional Notes

**Monitoring**: The pipeline includes Kafdrop for Kafka topic inspection, but production deployments should add:

- Prometheus + Grafana for metrics
- ELK stack for centralized logging
- Airflow SLAs for pipeline health alerts

**Scalability**: The current architecture supports:

- Horizontal scaling of Kafka producers/consumers
- Airflow worker parallelization
- PostgreSQL read replicas for query offloading

**Data Retention**: Configure retention policies based on requirements:

- Kafka: 7-day message retention (configurable)
- MinIO: Indefinite raw data storage
- PostgreSQL: Archive old partitions to cold storage
