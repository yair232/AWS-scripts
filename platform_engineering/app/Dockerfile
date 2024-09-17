FROM tiangolo/uwsgi-nginx-flask

WORKDIR /app

COPY ../CLI/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY ../CLI/ec2_manegment.py .
COPY ../CLI/route53_manegment.py .
COPY ../CLI/s3_manegment.py .

EXPOSE 2310

ENTRYPOINT ["python", "app.py"]