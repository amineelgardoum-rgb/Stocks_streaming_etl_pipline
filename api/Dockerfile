FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt
ENV PYTHONPATH="/app"
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
