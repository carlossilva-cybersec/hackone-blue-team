#!/bin/bash

echo "Instalando Docker..."
curl https://get.docker.com | bash 
echo "Instalando OpenVAS..."

cd /opt
wget Modulo 7 - Threat Prevention/scripts/compose.yaml