FROM python:3.11.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD alembic upgrade head; python src/main.py