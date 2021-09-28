FROM python:3.9.7-alpine

RUN ["mkdir", "/usr/share/quick_api"]
WORKDIR /usr/share/quick_api

COPY config.py config.py
COPY data/data.json data.json
COPY requirements.txt requirements.txt
COPY quick_api/ quick_api/
COPY data/ data/

RUN ["pip", "install", "-r", "requirements.txt"]

CMD ["gunicorn", "-w", "4", "-b", ":80", "quick_api:app"]
