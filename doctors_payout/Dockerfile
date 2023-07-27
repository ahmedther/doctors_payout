FROM python:3.11.3-slim as builder


ENV PYTHONUNBUFFERED 1

WORKDIR /doctors_payout

COPY ./requirements.txt ./


RUN apt update -y \
    && apt install  libpq-dev gcc libaio1  -y \ 
    && python3 -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install --no-cache --no-cache-dir -r ./requirements.txt  \
    && apt-get purge -y curl  unzip libpq-dev gcc libaio1 \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt autoremove -y  


FROM python:3.11.3-slim

ENV PYTHONUNBUFFERED 1

COPY --from=builder /py /py

WORKDIR /doctors_payout

COPY ./ ./


RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 rabbitmq-server curl unzip libaio1 \
    && mkdir -p /cx_oracle \
    && cd /cx_oracle \
    && curl -o instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip https://download.oracle.com/otn_software/linux/instantclient/219000/instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
    && unzip -d . instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
    && rm -f instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
    && echo /cx_oracle/instantclient_21_9 > /etc/ld.so.conf.d/oracle-instantclient.conf  \
    && ldconfig \
    && ln -snf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && echo Asia/Kolkata > /etc/timezone \
    && mkdir /var/log/uwsgi \
    && touch /var/log/uwsgi/doctors_payout.log \
    && apt-get purge -y curl  unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt autoremove -y  


LABEL maintainer='ahmed'


ENV LD_LIBRARY_PATH=/cx_oracle/instantclient_21_9

ENV PATH="/doctors_payout/scripts:/py/bin:$PATH"

EXPOSE 8008

CMD ["./scripts/py_run.sh"]