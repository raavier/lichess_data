# 🤖 Automação - Lichess Daily Download

## Como Configurar a Execução Automática Diária

### Opção 1: Configuração Automática (Recomendado)

1. **Abra o PowerShell como Administrador**
   - Pressione `Win + X`
   - Selecione "Windows PowerShell (Admin)" ou "Terminal (Admin)"

2. **Execute o script de configuração**
   ```powershell
   cd c:\jobs\lichess_data
   PowerShell -ExecutionPolicy Bypass -File setup_scheduler.ps1
   ```

3. **Pronto!** O script agora rodará automaticamente todos os dias às 23:00

### Opção 2: Configuração Manual

1. **Abra o Agendador de Tarefas**
   - Pressione `Win + R`
   - Digite: `taskschd.msc`
   - Pressione Enter

2. **Crie uma Nova Tarefa**
   - Clique em "Criar Tarefa..." (no painel direito)

3. **Aba "Geral"**
   - Nome: `Lichess Daily Download`
   - Descrição: `Baixa jogos diários do Lichess automaticamente`
   - Marque: "Executar estando o usuário conectado ou não"
   - Marque: "Executar com privilégios mais altos"

4. **Aba "Gatilhos"**
   - Clique em "Novo..."
   - Escolha: "Diariamente"
   - Horário: `23:00:00` (ou o horário que preferir)
   - Marque: "Ativado"

5. **Aba "Ações"**
   - Clique em "Novo..."
   - Ação: "Iniciar um programa"
   - Programa/script: `c:\jobs\lichess_data\run_daily.bat`
   - Iniciar em: `c:\jobs\lichess_data`

6. **Aba "Condições"**
   - Desmarque: "Iniciar a tarefa apenas se o computador estiver conectado à energia CA"
   - Marque: "Iniciar somente se a seguinte conexão de rede estiver disponível: Qualquer conexão"

7. **Aba "Configurações"**
   - Marque: "Executar tarefa o mais breve possível após uma inicialização agendada ser perdida"

8. **Clique em "OK"** para salvar

## Como Funciona

### Script Principal: `download_and_push.py` 🚀
- ✅ Baixa **TODOS** os jogos Blitz desde **01/08/2025**
- ✅ Sobrescreve arquivos existentes (mantém sempre atualizado)
- ✅ Organiza automaticamente por categoria
- ✅ **Faz commit automático no Git**
- ✅ **Push automático para repositório remoto**
- ✅ Registra execução em log

### Script Alternativo (sem Git): `download_daily.py`
- Use este se quiser apenas baixar sem enviar para o Git

### Arquivos de Automação

```
lichess_data/
├── download_and_push.py    # Script principal com Git (Python)
├── download_daily.py       # Script sem Git (Python)
├── run_daily.bat           # Executor (Batch) - chamado pelo agendador
├── setup_scheduler.ps1     # Configurador automático (PowerShell)
├── logs/
│   └── daily_run.log      # Histórico de execuções
└── pgn_games/
    └── blitz/             # Jogos baixados
```

## Testando Manualmente

Para testar sem esperar o horário agendado:

```batch
# Execute no terminal
cd c:\jobs\lichess_data
.\run_daily.bat
```

Ou execute diretamente o Python:
```batch
# Com Git push automático (RECOMENDADO)
python download_and_push.py

# Sem Git (apenas download)
python download_daily.py
```

## Verificando os Logs

### Ver últimas 50 linhas do log:
```powershell
Get-Content logs\daily_run.log -Tail 50
```

### Ver todo o log:
```powershell
Get-Content logs\daily_run.log
```

### Limpar o log:
```powershell
Clear-Content logs\daily_run.log
```

## Verificando a Tarefa Agendada

### Ver se está ativa:
```powershell
Get-ScheduledTask -TaskName "Lichess Daily Download"
```

### Ver histórico de execuções:
```powershell
Get-ScheduledTask -TaskName "Lichess Daily Download" | Get-ScheduledTaskInfo
```

### Executar manualmente agora:
```powershell
Start-ScheduledTask -TaskName "Lichess Daily Download"
```

### Desativar (sem remover):
```powershell
Disable-ScheduledTask -TaskName "Lichess Daily Download"
```

### Reativar:
```powershell
Enable-ScheduledTask -TaskName "Lichess Daily Download"
```

### Remover completamente:
```powershell
Unregister-ScheduledTask -TaskName "Lichess Daily Download" -Confirm:$false
```

## Customizações

### Mudar o horário de execução

Edite o arquivo `setup_scheduler.ps1` e mude esta linha:
```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At "23:00"
```

Para outro horário, por exemplo 08:00 da manhã:
```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00"
```

Depois execute novamente o script.

### Mudar a data inicial

Edite o arquivo `download_daily.py` e mude esta linha:
```python
START_DATE = datetime(2025, 8, 1)  # 01/08/2025
```

### Adicionar outros tipos de jogo

Edite o arquivo `download_daily.py` e mude:
```python
perf_types=["blitz"]
```

Para:
```python
perf_types=["blitz", "rapid", "bullet"]
```

### Baixar jogos de outro usuário

Edite o arquivo `download_daily.py` e mude:
```python
USERNAME = "r4v1"
```

## Observações Importantes

⚠️ **O computador precisa estar ligado** no horário agendado para executar

⚠️ **É necessária conexão com internet** para baixar os jogos e fazer push

⚠️ **Configure o Git antes** de usar o script automático:
```bash
git config user.name "Seu Nome"
git config user.email "seu@email.com"
```

⚠️ **Autenticação Git**: Configure suas credenciais ou use SSH para evitar pedir senha

✅ **Arquivos duplicados são sobrescritos** - não haverá duplicatas

✅ **Os logs ficam em** `logs/daily_run.log` para auditoria

✅ **Commits automáticos** com mensagem descritiva e timestamp

## Solução de Problemas

### A tarefa não executa
1. Verifique se o Python está no PATH do sistema
2. Teste executando `python --version` no CMD
3. Verifique os logs em `logs/daily_run.log`

### Erro de permissão
1. Execute o PowerShell como Administrador
2. Use o comando: `Set-ExecutionPolicy RemoteSigned`

### Não encontra o Python
1. Edite `run_daily.bat` e use o caminho completo:
   ```batch
   C:\Python314\python.exe download_and_push.py >> logs\daily_run.log 2>&1
   ```

### Erro ao fazer push (Git)
1. Verifique se o repositório remoto está configurado:
   ```bash
   git remote -v
   ```
2. Configure autenticação (use token ou SSH):
   ```bash
   # Para HTTPS com token
   git remote set-url origin https://<TOKEN>@github.com/<USER>/<REPO>.git

   # Ou use SSH (recomendado)
   git remote set-url origin git@github.com:<USER>/<REPO>.git
   ```
3. Teste manualmente:
   ```bash
   git push
   ```

## Suporte

Se tiver problemas:
1. Verifique o log: `logs\daily_run.log`
2. Teste manualmente: `python download_daily.py`
3. Verifique a tarefa: Agendador de Tarefas → Biblioteca do Agendador de Tarefas
