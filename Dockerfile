FROM rasa/rasa-sdk:3.6.2

WORKDIR /app
COPY  ./requirements.txt

USER root
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
COPY ./actions


USER 1001
