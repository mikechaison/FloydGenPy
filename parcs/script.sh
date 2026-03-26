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