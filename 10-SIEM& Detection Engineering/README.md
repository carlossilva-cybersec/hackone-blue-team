# SIEM Lab — Pós-Graduação Blue Team

> Laboratório de SIEM e Engenharia de Detecção de Ameaças  
> Stack open-source containerizada: **Fluentd → Data Prepper → OpenSearch + Dashboards**

---

## Objetivo

Ambiente de laboratório para prática de:

- Coleta e normalização de logs de aplicações e infraestrutura
- Engenharia de pipelines de ingestão de dados
- Criação e tuning de regras de detecção de ameaças
- Visualização e investigação de incidentes via dashboards
- Fundamentos de operação de um SOC moderno

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        SIEM Lab                             │
│                                                             │
│  Aplicação / Infra                                          │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────┐    forward/HTTP    ┌──────────────┐           │
│  │ Fluentd  │ ─────────────────▶ │ Data Prepper │           │
│  │ :24224   │                    │    :2021     │           │
│  │ :9880    │                    │  (pipeline)  │           │
│  └──────────┘                    └──────┬───────┘           │
│                                         │                   │
│                                         ▼                   │
│                                  ┌────────────┐             │
│                                  │ OpenSearch │             │
│                                  │   :9200    │             │
│                                  └─────┬──────┘             │
│                                        │                   │
│                                        ▼                   │
│                               ┌──────────────────┐         │
│                               │    Dashboards    │         │
│                               │     :5601        │         │
│                               └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

| Componente | Versão | Função |
|---|---|---|
| **Fluentd** | v1.16 | Coleta, parse e enriquecimento de logs |
| **Data Prepper** | 2.8.0 | Pipeline de processamento e indexação |
| **OpenSearch** | 2.14.0 | Motor de busca e armazenamento de logs |
| **OpenSearch Dashboards** | 2.14.0 | Visualização e análise de eventos |

---

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) >= 24.x
- [Docker Compose](https://docs.docker.com/compose/) >= 2.x
- Mínimo **4 GB de RAM** disponível para os containers
- Porta `5601`, `9200`, `2021`, `4900`, `24224` e `9880` livres

---

## Início Rápido

### 1. Clonar e configurar variáveis

```bash
git clone <url-do-repositorio>
cd "002 - siem"
cp .env.example .env   # ajuste as variáveis conforme necessário
```

### 2. Subir o ambiente

```bash
docker compose up -d
```

### 3. Verificar os serviços

```bash
docker compose ps
```

Aguarde todos os serviços estarem `healthy` antes de prosseguir (pode levar ~2 min na primeira execução).

### 4. Acessar o Dashboards

```
URL:    http://localhost:5601
```

> As credenciais de acesso estão definidas no arquivo `.env`.

---

## Estrutura do Projeto

```
002 - siem/
├── docker-compose.yml              # Orquestração dos serviços
├── .env                            # Variáveis de ambiente (não versionar!)
├── .env.example                    # Template de variáveis
└── config/
    ├── fluentd/
    │   ├── Dockerfile              # Imagem customizada do Fluentd
    │   └── fluent.conf             # Regras de coleta, parse e roteamento
    └── data-prepper/
        ├── pipelines.yaml          # Pipeline de ingestão e indexação
        └── data-prepper-config.yaml # Configuração global do Data Prepper
```

---

## Pipeline de Dados

### Fluentd (`config/fluentd/fluent.conf`)

O Fluentd é o ponto de entrada dos logs. Ele recebe eventos via:

| Entrada | Protocolo | Porta | Uso |
|---|---|---|---|
| Docker log driver | Forward (TCP) | `24224` | Logs de containers |
| Testes manuais | HTTP/JSON | `9880` | Injeção ad-hoc em aula |

Após a coleta, aplica:
1. **Parse** — extrai campos estruturados do payload JSON
2. **Enriquecimento** — adiciona metadados como `fluentd_tag` e `collector_host`
3. **Forward** — envia para o Data Prepper via HTTP

**Injeção manual de evento (útil para testes em aula):**

```bash
curl -X POST http://localhost:9880/siem.test \
     -H 'Content-Type: application/json' \
     -d '{"message":"login suspeito","src_ip":"10.0.0.99","user":"admin"}'
```

### Data Prepper (`config/data-prepper/pipelines.yaml`)

Recebe os logs do Fluentd, aplica processadores e indexa no OpenSearch:

```
HTTP :2021 → [date processor] → [parse_xml] → OpenSearch index: siem-logs
```

---

## Exercícios Sugeridos

### Nível 1 — Coleta e Normalização

- [ ] Injetar eventos manualmente via HTTP e validar no OpenSearch Dashboards
- [ ] Adicionar um novo campo de enriquecimento no `fluent.conf`
- [ ] Criar um segundo índice no pipeline para separar logs por fonte

### Nível 2 — Detecção de Ameaças

- [ ] Criar um dashboard no Dashboards para monitorar tentativas de login (`user`, `status`, `src_ip`)
- [ ] Construir uma alerta para múltiplas falhas de autenticação (brute force)
- [ ] Mapear os campos coletados para o framework **MITRE ATT&CK**

### Nível 3 — Engenharia Avançada

- [ ] Adicionar um novo serviço ao `docker-compose.yml` (ex.: Filebeat, Logstash)
- [ ] Implementar enriquecimento com GeoIP nos logs de rede
- [ ] Criar regras de correlação para detecção de movimentação lateral

---

## Comandos Úteis

```bash
# Ver logs de um serviço
docker compose logs -f fluentd
docker compose logs -f data-prepper
docker compose logs -f opensearch

# Parar o ambiente (preserva dados)
docker compose stop

# Derrubar e remover volumes (reset completo)
docker compose down -v

# Verificar saúde do Data Prepper
curl http://localhost:4900/health

# Verificar saúde do OpenSearch
curl -sk https://localhost:9200 -u admin:<senha>
```

---

## Referências

- [OpenSearch Documentation](https://opensearch.org/docs/)
- [Data Prepper Documentation](https://opensearch.org/docs/latest/data-prepper/)
- [Fluentd Documentation](https://docs.fluentd.org/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Sigma Rules](https://github.com/SigmaHQ/sigma) — regras de detecção open-source

---

## Avisos

> **Ambiente educacional.** Não expor esta stack na internet sem configurar TLS, autenticação forte e segmentação de rede adequadas.
>
> O arquivo `.env` contém credenciais — nunca suba este arquivo para repositórios públicos.
