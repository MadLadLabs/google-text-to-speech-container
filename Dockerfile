FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install \
    pyyaml

RUN pip3 install --upgrade \
    google-cloud-texttospeech

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json

COPY /src /app

WORKDIR /app

CMD python3 app.py