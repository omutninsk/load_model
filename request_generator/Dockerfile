FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .
COPY templates templates
COPY entrypoint.sh .
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
CMD ["python", "app.py"]