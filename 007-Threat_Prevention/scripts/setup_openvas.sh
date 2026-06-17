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
# Verificação Docker Compose
# ==========================
if ! docker compose version >/dev/null 2>&1; then
    error "Docker Compose não encontrado."
    exit 1
fi

# ==========================
# Download dos arquivos
# ==========================
log "Criando diretório de instalação..."

mkdir -p "$WORKDIR"

log "Baixando docker-compose.yaml..."

wget -q "$COMPOSE_URL" -O "$WORKDIR/docker-compose.yaml"

if [[ ! -s "$WORKDIR/docker-compose.yaml" ]]; then
    error "Falha ao baixar docker-compose.yaml"
    exit 1
fi

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
# Senha do administrador
# ==========================
PASSWORD=""

while [[ -z "$PASSWORD" ]]; do
    echo
    read -r -s -p "Defina uma senha para o usuário admin: " PASSWORD
done

echo

# ==========================
# Aguardar gvmd ficar pronto
# ==========================
log "Aguardando inicialização do Greenbone (isso pode levar alguns minutos)..."

MAX_ATTEMPTS=60
ATTEMPT=1

until docker compose exec -u gvmd gvmd gvmd --get-users >/dev/null 2>&1; do
    if [[ $ATTEMPT -ge $MAX_ATTEMPTS ]]; then
        error "Tempo limite excedido aguardando o serviço gvmd."
        error "Verifique os logs com:"
        error "cd $WORKDIR && docker compose logs -f"
        exit 1
    fi

    echo "    Tentativa $ATTEMPT/$MAX_ATTEMPTS..."
    sleep 30
    ((ATTEMPT++))
done

# ==========================
# Configuração da senha
# ==========================
log "Configurando senha do usuário admin..."

docker compose exec -u gvmd gvmd \
    gvmd --user=admin --new-password="$PASSWORD"

# ==========================
# Finalização
# ==========================
echo
log "Instalação concluída com sucesso!"
echo
echo "=========================================="
echo " OpenVAS / Greenbone Community Edition"
echo "=========================================="
echo
echo "URL: https://IP_DO_SERVIDOR:9392"
echo "Usuário: admin"
echo "Senha: Definida durante a instalação"
echo
echo "Diretório de instalação:"
echo "$WORKDIR"
echo
echo "Observação:"
echo "A sincronização inicial dos feeds pode levar alguns minutos."
echo