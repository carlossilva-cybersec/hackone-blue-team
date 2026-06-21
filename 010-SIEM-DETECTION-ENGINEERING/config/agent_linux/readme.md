# Fluent Bit — Instalação e Configuração Ubuntu

## 1. Adicionar a chave GPG do repositório

Adicione a chave GPG oficial do Fluent Bit ao sistema para garantir a autenticidade dos pacotes instalados.

```bash
sudo sh -c 'curl https://packages.fluentbit.io/fluentbit.key | gpg --dearmor > /usr/share/keyrings/fluentbit-keyring.gpg'
```

---

## 2. Identificar a versão do Ubuntu

Execute o comando abaixo para identificar automaticamente o codinome da sua distribuição Ubuntu:

```bash
codename=$(grep -oP '(?<=VERSION_CODENAME=).*' /etc/os-release 2>/dev/null || lsb_release -cs 2>/dev/null)
```

---

## 3. Adicionar o repositório do Fluent Bit

Adicione o repositório oficial à lista de fontes do APT:

```bash
echo "deb [signed-by=/usr/share/keyrings/fluentbit-keyring.gpg] https://packages.fluentbit.io/ubuntu/$codename $codename main" | sudo tee /etc/apt/sources.list.d/fluent-bit.list
```

---

## 4. Atualizar a lista de pacotes

Atualize a base de dados dos repositórios:

```bash
sudo apt update
```

---

## 5. Instalar o Fluent Bit

Instale o Fluent Bit utilizando o gerenciador de pacotes:

```bash
sudo apt install fluent-bit -y
```

---

## 6. Verificar a instalação

Confirme se o Fluent Bit foi instalado corretamente:

```bash
fluent-bit --version
```

---

## 7. Iniciar o serviço

Habilite e inicie o serviço:

```bash
sudo systemctl enable fluent-bit
sudo systemctl start fluent-bit
```

Verifique o status:

```bash
sudo systemctl status fluent-bit
```

---



# Referências
* Documentação Oficial: https://docs.fluentbit.io
* Site Oficial: https://fluentbit.io
