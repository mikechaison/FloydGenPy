FROM python:3-slim

WORKDIR /app

RUN pip install --no-cache-dir docker

COPY ./parcs ./parcs
COPY ./runner/main.py ./main.py
COPY ./runner/matrix.json ./matrix.json

ENV PYTHONPATH=/app
ENV DOCKER_API_VERSION=1.40
ENV PARCS_ADDR=10.128.0.51

CMD ["python", "main.py"]