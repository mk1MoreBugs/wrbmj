FROM python:slim

WORKDIR /backend

COPY ./app app
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8080

CMD uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload