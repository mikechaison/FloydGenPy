FROM python:3-slim

WORKDIR /app

RUN pip install --no-cache-dir docker

COPY ./parcs ./parcs
COPY ./worker/main.py ./main.py

ENV PYTHONPATH=/app
ENV PARCS_ADDR=10.128.0.51

CMD ["python", "main.py"]