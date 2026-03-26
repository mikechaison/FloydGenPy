# Distributed Floyd-Warshall Algorithm with Heterogeneous PARCS Python

This project implements a parallelized version of the **Floyd-Warshall algorithm** for solving the all-pairs shortest path problem. It leverages the **PARCS (Parallel Computing System)** framework, containerized with **Docker**, and orchestrated via **Docker Swarm**.

## 📌 Overview

The algorithm iteratively updates the shortest distance between all pairs of vertices. In this distributed implementation, each $k$-th iteration's matrix updates are split by rows and distributed among multiple worker nodes, significantly reducing execution time for large matrices.

## 🛠 Features

- **Heterogeneous Computing:** Distributed task execution using the PARCS framework.
- **Dockerized Infrastructure:** Separate images for Leader (Runner) and Worker (Service) nodes.
- **Scalable Performance:** Easily adjust the number of workers via environment variables.
- **Cloud Ready:** Tested on Google Cloud Platform (GCE) using `e2-standard-2` instances.
- **Monitoring:** Compatible with **Portainer** for real-time cluster visualization.

## 🚀 Deployment

### Prerequisites
- A Docker Swarm cluster.
- An overlay network named `parcs` taken from https://github.com/lionell/parcs/tree/master/py/parcs.

### Run the Leader Node
Execute the following command on your Swarm Manager to start the computation:

```bash
sudo docker service create \
    --name runner \
    --constraint 'node.role == manager' \
    --mount type=bind,source=$(pwd),target=/app/output \
    --network parcs \
    --restart-condition none \
    --env LEADER_URL=tcp://<MANAGER_IP>:4321 \
    --env WORKERS=4 \
    --env N=500 \
    --env SERVICE_IMAGE=mikechaison/floyd-gen-py-worker:latest \
    mikechaison/floyd-gen-py:latest