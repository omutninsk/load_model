FROM python:3.8-slim-buster

ENV FLASK_APP=app.py

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY app.py .

COPY entrypoint.sh .
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
CMD ["start"]