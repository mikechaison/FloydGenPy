FROM python:3-slim

WORKDIR /app

RUN pip install --no-cache-dir docker

COPY ./parcs ./parcs
COPY ./runner/main.py ./main.py
COPY ./runner/matrix.json ./matrix.json
COPY ./runner/matrix1.json ./matrix1.json
COPY ./runner/matrix2.json ./matrix2.json

ENV PYTHONPATH=/app
ENV DOCKER_API_VERSION=1.40
ENV PARCS_ADDR=10.128.0.51

CMD ["python", "main.py"]