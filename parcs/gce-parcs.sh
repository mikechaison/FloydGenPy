#!/usr/bin/env bash

set -e

RED='\033[0;31m'
NC='\033[0m'

function tell() {
    echo -e "${RED}$1${NC}"
}

function install_docker() {
    gcloud compute ssh $1 --command "curl -fsSL https://get.docker.com | sudo sh"
    tell "Docker installed on $1"
}

read -p "Number of workers: " num_workers
if [ $num_workers -lt 1 ]
then
    tell "Cluster should contain at least 1 worker."
    exit 1
fi

workers=()
for i in $(seq $num_workers)
do
    workers+=("worker-${i}")
done

gcloud compute instances create leader ${workers[@]}
tell "GCE instances for leader and ${num_workers} workers created."

install_docker "leader"
for i in ${workers[@]}
do
    install_docker "${i}"
done

gcloud compute ssh leader --command "sudo docker swarm init"
token=$(gcloud compute ssh leader --command "sudo docker swarm join-token worker" | grep "docker swarm join")
for i in ${workers[@]}
do
    gcloud compute ssh $i --command "sudo $token"
done
tell "Docker Swarm initialized"

gcloud compute ssh leader --command "sudo sed -i '/ExecStart/ s/$/ -H tcp:\/\/0.0.0.0:4321/' /lib/systemd/system/docker.service \
       && sudo systemctl daemon-reload \
       && sudo systemctl restart docker"
tell "PARCS port (4321) is open on leader"

gcloud compute ssh leader --command "sudo docker network create -d overlay parcs"
tell "Overlay network created for PARCS"

tell "Installing Portainer CE..."
gcloud compute ssh leader --command "sudo mkdir -p /var/lib/portainer/data && \
    sudo curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml && \
    sudo docker stack deploy -c portainer-agent-stack.yml portainer"
tell "Portainer deployed as a stack"

gcloud compute firewall-rules create portainer-rule --allow tcp:9443
tell "Firewall rule for Portainer (9443) created"

url=$(gcloud compute instances list | grep leader | awk '{print "https://" $5 ":9443"}')
leader_url=$(gcloud compute instances list | grep leader | awk '{print "tcp://" $4 ":4321"}')
tell "---------------------------------------"
tell "LEADER_URL=${leader_url}"
tell "Dashboard URL: ${url}"
tell "Login: admin"
tell "Password: adminpassword"
tell "---------------------------------------"
tell "DON'T FORGET TO DELETE ALL CREATED INSTANCES WHEN YOUR'RE DONE"
tell "$ gcloud compute instances delete leader ${workers[@]}"
tell "$ gcloud compute firewall-rules delete swarmpit"
