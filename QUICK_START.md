# 🚀 Quick Start - Automação Diária

## Teste Rápido (FAÇA ISSO PRIMEIRO!)

### 1. Teste o download básico
```bash
python download_and_push.py
```

Isso vai:
- ✅ Baixar jogos do Lichess
- ✅ Fazer commit no Git
- ✅ Fazer push para o GitHub

### 2. Se deu tudo certo, configure a automação

**Abra PowerShell como Administrador** e execute:
```powershell
cd c:\jobs\lichess_data
PowerShell -ExecutionPolicy Bypass -File setup_scheduler.ps1
```

### 3. Pronto! ✨

A partir de agora, **todos os dias às 23:00**, o script vai:
1. Baixar jogos novos do Lichess (desde 01/08/2025)
2. Adicionar ao Git
3. Fazer commit com mensagem automática
4. Fazer push para o GitHub

## Verificar se está funcionando

### Ver o log:
```powershell
Get-Content logs\daily_run.log -Tail 50
```

### Executar manualmente agora (sem esperar 23h):
```powershell
Start-ScheduledTask -TaskName "Lichess Daily Download"
```

### Ver status da tarefa:
```powershell
Get-ScheduledTask -TaskName "Lichess Daily Download"
```

## Solução Rápida de Problemas

### ❌ Erro ao fazer push

**Problema**: Git pede autenticação

**Solução 1** - Usar SSH (RECOMENDADO):
```bash
# Gere uma chave SSH se não tiver
ssh-keygen -t ed25519 -C "seu@email.com"

# Adicione ao GitHub: Settings → SSH Keys → New SSH Key
# Cole o conteúdo de: C:\Users\<seu-usuario>\.ssh\id_ed25519.pub

# Mude o remote para SSH
git remote set-url origin git@github.com:raavier/lichess_data.git
```

**Solução 2** - Usar Token de Acesso:
```bash
# Crie um token no GitHub: Settings → Developer Settings → Personal Access Tokens
# Marque a permissão "repo"

# Configure o remote com o token
git remote set-url origin https://<SEU-TOKEN>@github.com/raavier/lichess_data.git
```

### ❌ Tarefa não executa

1. Verifique se o computador estava **ligado** às 23:00
2. Verifique o log: `logs\daily_run.log`
3. Teste manualmente: `python download_and_push.py`

### ❌ Python não encontrado

Edite `run_daily.bat` e use o caminho completo do Python:
```batch
C:\Python314\python.exe download_and_push.py >> logs\daily_run.log 2>&1
```

## Customização Rápida

### Mudar horário

Edite `setup_scheduler.ps1`, linha:
```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At "23:00"
```

Mude para o horário desejado (ex: `"08:00"`) e execute novamente.

### Mudar data inicial

Edite `download_and_push.py`, linha:
```python
START_DATE = datetime(2025, 8, 1)  # 01/08/2025
```

### Adicionar mais tipos de jogo

Edite `download_and_push.py`, linha:
```python
perf_types=["blitz"]
```

Mude para:
```python
perf_types=["blitz", "rapid", "bullet"]
```

## Estrutura de Arquivos

```
lichess_data/
├── download_and_push.py    ← Script principal (download + git)
├── download_daily.py       ← Script sem git (só download)
├── download_r4v1.py        ← Script inicial de teste
├── run_daily.bat           ← Chamado pelo agendador
├── setup_scheduler.ps1     ← Configura agendador
├── QUICK_START.md          ← Este arquivo
├── AUTOMACAO_README.md     ← Documentação completa
├── logs/
│   └── daily_run.log       ← Log de execuções
└── pgn_games/
    └── blitz/              ← Jogos baixados
```

## Comandos Úteis

```powershell
# Testar agora
python download_and_push.py

# Ver log
Get-Content logs\daily_run.log -Tail 50

# Executar tarefa agendada agora
Start-ScheduledTask -TaskName "Lichess Daily Download"

# Ver status da tarefa
Get-ScheduledTask -TaskName "Lichess Daily Download"

# Desativar temporariamente
Disable-ScheduledTask -TaskName "Lichess Daily Download"

# Reativar
Enable-ScheduledTask -TaskName "Lichess Daily Download"

# Remover tarefa
Unregister-ScheduledTask -TaskName "Lichess Daily Download" -Confirm:$false
```

---

**Pronto! Seus jogos serão baixados e enviados ao GitHub automaticamente todos os dias! ♟️**
