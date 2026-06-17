## Instalação do OpenVAS (Greenbone Community Edition)

A instalação do OpenVAS é realizada automaticamente através do script `setup_openvas.sh`.

### Executando a instalação

```bash
curl -fsSL https://raw.githubusercontent.com/carlossilva-cybersec/hackone-blue-team/refs/heads/main/Modulo%207%20-%20Threat%20Prevention/scripts/setup_openvas.sh | sudo bash
```

Durante a execução será solicitada a definição da senha do usuário `admin`.

### O que o script faz

- Instala o Docker
- Baixa o arquivo `docker-compose.yaml`
- Realiza o download das imagens do Greenbone Community Edition
- Inicializa os containers
- Configura a senha do usuário `admin`

### Acesso à Interface Web

Após a instalação e inicialização dos serviços, acesse:

```
https://IP_DO_SERVIDOR:443
```

**Usuário:**

```
admin
```

**Senha:**

A senha definida durante a execução do script.

### Observações

- A primeira inicialização pode levar alguns minutos devido à sincronização dos feeds de vulnerabilidades.
- Certifique-se de que a porta `443/TCP` esteja liberada no firewall.
- Os arquivos serão instalados em:

```
/opt/greenbone-community-container
```