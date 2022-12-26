FROM apache/airflow:2.5.0
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
USER airflow
