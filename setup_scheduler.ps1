# Script PowerShell para configurar o Agendador de Tarefas
# Execute como Administrador: PowerShell -ExecutionPolicy Bypass -File setup_scheduler.ps1

$taskName = "Lichess Daily Download"
$scriptPath = "$PSScriptRoot\run_daily.bat"
$description = "Baixa jogos diários do Lichess automaticamente"

# Define o horário de execução (todos os dias às 23:00)
$trigger = New-ScheduledTaskTrigger -Daily -At "23:00"

# Define a ação (executar o script batch)
$action = New-ScheduledTaskAction -Execute "$scriptPath"

# Define configurações adicionais
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Registra a tarefa
try {
    # Remove tarefa existente se houver
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

    # Cria nova tarefa
    Register-ScheduledTask `
        -TaskName $taskName `
        -Trigger $trigger `
        -Action $action `
        -Settings $settings `
        -Description $description `
        -User $env:USERNAME

    Write-Host "✓ Tarefa '$taskName' criada com sucesso!" -ForegroundColor Green
    Write-Host "  Horário: Todos os dias às 23:00" -ForegroundColor Cyan
    Write-Host "  Script: $scriptPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Para testar manualmente, execute:" -ForegroundColor Yellow
    Write-Host "  .\run_daily.bat" -ForegroundColor White
    Write-Host ""
    Write-Host "Para ver os logs:" -ForegroundColor Yellow
    Write-Host "  Get-Content logs\daily_run.log -Tail 50" -ForegroundColor White
}
catch {
    Write-Host "✗ Erro ao criar tarefa: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Tente executar o PowerShell como Administrador" -ForegroundColor Yellow
}
