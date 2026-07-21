# 🐧 Exercicio — Linux Log Investigation and audit: CSBank Rootkit

## 📖 Cenário

A equipe de resposta a incidentes da **CSBank** identificou uma possível comprometedora em um dos servidores de produção. Durante a triagem inicial, foi encontrado um **rootkit** ativo no sistema.

Antes que o servidor fosse isolado da rede, a equipe conseguiu extrair uma cópia completa dos logs do sistema operacional. Esses artefatos agora estão em suas mãos.

Investigar logs desconhecidos é parte do dia a dia de quem responde a incidentes — não tenha medo de explorar, cruzar informações e testar hipóteses. Os logs sempre contam uma história; seu trabalho é reconstruí-la.

## 🎯 Sua missão

Analise os artefatos coletados e responda às perguntas abaixo.

| # | Pergunta | Categoria |
|---|----------|-----------|
| 1 | Algum novo serviço foi iniciado, instalado ou modificado com base nos logs? | Persistência |
| 2 | Existem atividades suspeitas, como execuções partindo do usuário `root`? | Escalonamento / Execução |
| 3 | Correlacionando os eventos, quais IPs tiveram interação com o protocolo SSH? | Rede / Acesso remoto |
| 4 | Qual foi o último usuário a fazer login no sistema operacional? | Linha do tempo / Logon |

## 🧰 Ferramentas sugeridas

Você pode (e deve) usar as ferramentas nativas do Linux para essa investigação:

- `journalctl` — logs do systemd
- `grep`, `awk`, `sed` — busca e parsing de texto
- `last`, `lastlog`, `who`, `w` — histórico e sessões de login
- `cat /var/log/auth.log` ou `/var/log/secure` — autenticação e SSH
- `ausearch` / `auditd` (se disponível) — trilha de auditoria


## 💡 Dicas

- Cruze os timestamps entre diferentes arquivos de log para montar uma linha do tempo coerente do ataque.
- Serviços de persistência de rootkits costumam aparecer como nomes genéricos ou muito parecidos com serviços legítimos.
- Nem toda atividade do usuário `root` é maliciosa — busque por padrões fora do horário/rotina esperada.

## ✅ Critério de conclusão

O desafio é considerado concluído quando as 4 perguntas forem respondidas com evidência de log anexada.

---
*Bons logs, boa caçada.* 🕵️‍♂️
