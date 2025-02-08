FROM python:3.13.2-slim

WORKDIR /backend

COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 8080

CMD uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload --proxy-headers

# HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=5 \
# CMD curl -f http://localhost:8080/v1/