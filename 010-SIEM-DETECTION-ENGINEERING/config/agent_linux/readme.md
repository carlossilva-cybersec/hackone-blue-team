# Fluent Bit — Instalação e Configuração no Windows

Coleta de Windows Event Logs (Security, System, Application) com envio para o Data Prepper via HTTP.

---

## Pré-requisitos

- Windows 10/Server 2016 ou superior (64 bits)
- PowerShell executado como **Administrador**
- Acesso ao Data Prepper em `192.168.15.200:2021`

---

## 1. Download do Binário

Baixe o instalador da versão 5.0.7:

```
https://packages.fluentbit.io/windows/fluent-bit-5.0.7-win64.exe
```

---

## 2. Instalação

Execute o instalador como Administrador. O padrão instala em:

```
C:\Program Files\fluent-bit\
```

---

## 3. Criação dos Diretórios de Dados

O Fluent Bit precisa de diretórios para o storage e para os arquivos de banco de dados (controle de offset dos logs).

Abra o PowerShell como **Administrador** e execute:

```powershell
New-Item -ItemType Directory -Force -Path "C:\fluent-bit\storage"
New-Item -ItemType Directory -Force -Path "C:\fluent-bit\db"
```

---

## 4. Configuração

Substitua o arquivo de configuração padrão pelo arquivo deste repositório.

Copie `fluent-bit.conf` para:

```
C:\Program Files\fluent-bit\conf\fluent-bit.conf
```

Via PowerShell (ajuste o caminho de origem conforme necessário):

```powershell
Copy-Item "fluent-bit.conf" -Destination "C:\Program Files\fluent-bit\conf\fluent-bit.conf" -Force
```

### O que a configuração faz

| Seção | Detalhe |
|---|---|
| **INPUT winlog** | Coleta os canais `Security`, `System` e `Application` |
| **FILTER modify** | Adiciona `hostname`, `source`, `event_source` e `event_type` a todos os eventos |
| **OUTPUT stdout** | Imprime logs no console — útil durante implantação (pode remover em produção) |
| **OUTPUT http** | Envia eventos para o Data Prepper em `192.168.15.200:2021/log/ingest` |

---

## 5. Teste Manual (antes de criar o serviço)

Valide a configuração executando o Fluent Bit diretamente no terminal:

```powershell
& "C:\Program Files\fluent-bit\bin\fluent-bit.exe" -c "C:\Program Files\fluent-bit\conf\fluent-bit.conf"
```

Verifique se logs dos canais Windows aparecem no stdout sem erros. Use `Ctrl+C` para parar.

---

## 6. Criação do Serviço Windows

Registre o Fluent Bit como serviço para inicialização automática.

### Opção A — New-Service (recomendado no PowerShell)

```powershell
sc.exe create fluent-bit --% binPath= "\"C:\Program Files\fluent-bit\bin\fluent-bit.exe\" -c \"C:\Program Files\fluent-bit\conf\fluent-bit.conf\"" start= auto DisplayName= "Fluent Bit Log Collector"
```

```

---
## 7. Gerenciamento do Serviço

```powershell
# Iniciar
sc.exe start fluent-bit

# Verificar status
sc.exe query fluent-bit

# Parar
sc.exe stop fluent-bit

# Remover o serviço (se necessário)
sc.exe delete fluent-bit
```

---

## 8. Verificação

Confirme que os eventos estão chegando ao Data Prepper:

```powershell
# Testa conexão com o Data Prepper
Test-NetConnection -ComputerName "IP DO SIEM" -Port 2021
```

---
---

## Estrutura de Arquivos

```
C:\Program Files\fluent-bit\
└── conf\
    └── fluent-bit.conf    ← arquivo de configuração

C:\fluent-bit\
├── storage\               ← buffer de disco do Fluent Bit
└── db\
    ├── security.db        ← offset do canal Security
    ├── system.db          ← offset do canal System
    └── application.db     ← offset do canal Application
```
