# Builder Stage
FROM python:latest AS builder

WORKDIR /app

COPY ./config.json ./requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN pyinstaller --clean --onefile --add-data config.json:. --distpath . main.py

# CMD [ "./HTTPmonitor" ]



# Runner Stage
FROM alpine:3.18 AS runner

WORKDIR /app

COPY --from=builder /app/main /app/config.json /app/

CMD [ "./main" ]
