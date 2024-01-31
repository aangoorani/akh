FROM python:alpine3.19 AS builder

WORKDIR /app

COPY ./config.json ./requirements.txt /app/

RUN apk update && \
apk add --no-cache \
build-base \
libffi-dev \
openssl-dev \
python3-dev

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install pyinstaller

COPY . /app/

RUN pyinstaller --clean --onefile --add-data config.json:. --name HTTPmonitor --distpath . main.py

FROM alpine:3.19 as runner

WORKDIR /app

COPY --from=builder /app/HTTPmonitor /app/config.json /app/

CMD [ "./HTTPmonitor" ]