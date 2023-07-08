FROM python:3.11.4-slim-bookworm

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install --no-install-recommends -y \
     gcc \
     libc6-dev \
     \
     && pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt \
     \
     && apt-get remove -y gcc \
     && apt autoremove -y \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p staticfiles mediafiles \
     && groupadd -r web && useradd -d /opt/app -r -g web web \
     && chown web:web -R /opt/app

USER web

ENTRYPOINT ["/opt/app/entrypoint.sh"]

