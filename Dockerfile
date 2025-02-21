FROM apache/airflow:latest-python3.12

USER root
# Install chrome and chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && mkdir -p /tmp/chrome-data \
    && chmod 777 /tmp \
    && chmod 777 /tmp/chrome-data

USER airflow
COPY --chown=airflow:root requirements.txt /requirements.txt
RUN pip install -r /requirements.txt