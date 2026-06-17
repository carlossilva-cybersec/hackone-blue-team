#!/bin/bash

echo "Instalando Docker..."
curl https://get.docker.com | bash 
echo "Instalando OpenVAS..."

curl -f -O https://greenbone.github.io/docs/latest/_static/setup-and-start-greenbone-community-edition.sh && 
chmod u+x setup-and-start-greenbone-community-edition.sh
./setup-and-start-greenbone-community-edition.sh