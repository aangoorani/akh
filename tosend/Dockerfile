# Builder Stage
FROM python:latest AS builder

WORKDIR /app

COPY ./config.json ./requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN pyinstaller --clean --onefile --add-data config.json:. --distpath . main.py

# Final Stage
FROM python:slim

WORKDIR /app

COPY --from=builder /app/main /app/config.json /app/

# COPY --from=builder /app/main /app
# COPY --from=builder  /app/config.json /app

CMD [ "/app/main" ]
