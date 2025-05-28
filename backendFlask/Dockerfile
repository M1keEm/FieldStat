FROM python:3.10-slim

WORKDIR /backendFlask

COPY optimized-requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "db", "init"]

CMD ["flask", "db", "migrate", "-m", "migrate all"]

CMD ["flask", "db", "upgrade"]

CMD ["flask", "run"]