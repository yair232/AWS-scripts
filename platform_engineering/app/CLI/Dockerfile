FROM python:3.9-slim
WORKDIR /platform_engineering
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "main.py"]