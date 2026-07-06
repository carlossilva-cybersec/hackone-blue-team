FROM python:3.10-slim

WORKDIR /app

COPY app.py ./
COPY templates ./templates
COPY raw_xml ./raw_xml

RUN pip install --no-cache-dir flask

EXPOSE 5000

CMD ["python", "app.py"]
