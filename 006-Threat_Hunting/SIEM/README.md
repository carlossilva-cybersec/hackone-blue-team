# Threat Hunting Queries SIEM

Uma aplicação Flask didática que simula uma interface de SIEM focada em threat hunting usando logs em XML.

## Recursos
- leitura de logs Sysmon em `raw_xml/registry_persistance.xml`
- consultas no estilo EQL simplificado
- painel com contagem de eventos, linha do tempo e tabela de logs
- detalhe expandido com todos os campos do evento e raw log XML
- deployment fácil via Docker

## Estrutura
- `app.py` - aplicação Flask principal
- `templates/` - views HTML para dashboard e resultados
- `raw_xml/` - logs de entrada em XML
- `tests/` - testes de validação
- `Dockerfile` - container Docker para deploy
- `.dockerignore` - arquivos ignorados no build do container

## Requisitos
- Docker instalado
- ou Python 3.10 e Flask

## Executar localmente
```bash
python app.py
```
Acesse: `http://127.0.0.1:5000`

## Executar com Docker
```bash
docker build -t threat-hunting-siem .
docker run --rm -p 5000:5000 threat-hunting-siem
```
Acesse: `http://127.0.0.1:5000`

## Executar testes
```bash
python -m pytest
```

## Notas
- Use `query` no formulário para buscar logs.
- Exemplo: `event_id == 13`, `image contains 'svchost'`, `target_object contains 'Services'`.
