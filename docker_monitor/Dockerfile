FROM python:3-11.slim
WORKDIR /app
COPY requirements.txt . 
RUN pip install -r requirements.txt --timeout 100
COPY . .
CMD ["python","-u","main.py"]