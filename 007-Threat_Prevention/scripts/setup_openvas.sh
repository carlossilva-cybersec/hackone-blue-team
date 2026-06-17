#!/usr/bin/env bash

set -euo pipefail

# ==========================
# Configurações
# ==========================
WORKDIR="/opt/greenbone-community-container"
COMPOSE_URL="https://raw.githubusercontent.com/carlossilva-cybersec/hackone-blue-team/refs/heads/main/007-Threat_Prevention/scripts/files/compose.yaml"

# ==========================
# Funções
# ==========================
log() {
    echo "[+] $1"
}

error() {
    echo "[!] $1" >&2
}

# ==========================
# Verificação de privilégios
# ==========================
if [[ $EUID -ne 0 ]]; then
    error "Execute este script como root."
    exit 1
fi

# ==========================
# Instalação do Docker
# ==========================
log "Instalando Docker..."

curl -fsSL https://get.docker.com | bash

# ==========================
# Download dos arquivos
# ==========================
log "Criando diretório de instalação..."

mkdir -p "$WORKDIR"

log "Baixando docker-compose.yaml..."

wget -q \
    "$COMPOSE_URL" \
    -O "$WORKDIR/docker-compose.yaml"

# ==========================
# Download das imagens
# ==========================
log "Baixando imagens do Greenbone..."

cd "$WORKDIR"

docker compose pull

# ==========================
# Inicialização do ambiente
# ==========================
log "Iniciando containers..."

docker compose up -d

# ==========================
# Definição da senha admin
# ==========================
echo
read -r -s -p "Defina uma senha para o usuário admin: " PASSWORD
echo

log "Configurando senha do usuário admin..."

docker compose exec -u gvmd gvmd \
    gvmd --user=admin --new-password="$PASSWORD"

echo
log "Instalação concluída com sucesso!"
log "Aguarde alguns minutos para a inicialização completa dos serviços."