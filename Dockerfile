FROM python:2.7-buster
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV USER=docker \
    GROUP=docker \
    UID=12345 \
    GID=23456 \
    HOME=/usr/src/app \
    PYTHONUNBUFFERED=1 \
    UWSGI_MODULE=api:app \
    UWSGI_PROCESSES=1 \
    UWSGI_THREADS=2 \
    UWSGI_OFFLOAD_THREADS=2

EXPOSE 5051
EXPOSE 5678
ENTRYPOINT [ "uwsgi", "--ini", "uwsgi.ini" ]