FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apt-get update \
     && apt-get install --no-install-recommends -y netcat=1.10-46 \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p staticfiles mediafiles \ 
     && groupadd -r web && useradd -d /opt/app -r -g web web \
     && chown web:web -R /opt/app

USER web

ENTRYPOINT ["/opt/app/entrypoint.sh"]
