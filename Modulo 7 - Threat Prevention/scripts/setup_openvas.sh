#!/bin/bash

echo "Instalando Docker..."
curl https://get.docker.com | bash 
echo "Instalando OpenVAS..."
cd /opt
mkdir greenbone-community-container 

wget https://raw.githubusercontent.com/carlossilva-cybersec/hackone-blue-team/refs/heads/main/Modulo%207%20-%20Threat%20Prevention/scripts/compose.yaml

docker compose build 