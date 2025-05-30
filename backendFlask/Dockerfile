FROM python:3.10-slim

WORKDIR /backendFlask

COPY optimized-requirements.txt requirements.txt

# Install netcat for the database connection check
RUN apt-get update && apt-get install -y netcat-openbsd && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Make entrypoint script executable
RUN chmod +x /backendFlask/entrypoint.sh

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

# Use entrypoint script instead of direct flask command
ENTRYPOINT ["/backendFlask/entrypoint.sh"]

