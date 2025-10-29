FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt 
ENV PYTHONPATH="/app"
CMD ["python","-u","producer.py"]
