#!/usr/bin/env python3
"""
Script automático para baixar jogos diariamente E enviar para o Git
Baixa jogos a partir de 01/08/2025 e faz commit/push automático
"""

from datetime import datetime
from lichess_downloader import LichessDownloader
import subprocess
import sys

# Configurações
USERNAME = "r4v1"
START_DATE = datetime(2025, 8, 1)  # 01/08/2025

# Calcula o timestamp da data inicial
since = int(START_DATE.timestamp() * 1000)

print("="*60)
print("  LICHESS DAILY UPDATE + GIT PUSH")
print("="*60)
print(f"Usuario: {USERNAME}")
print(f"Baixando jogos desde: {START_DATE.strftime('%d/%m/%Y')}")
print(f"Tipo: Blitz")
print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("="*60)

try:
    # Cria o downloader
    downloader = LichessDownloader(USERNAME)

    # Baixa os jogos
    print("\n>> Iniciando download...")
    pgn_content = downloader.download_games(
        since=since,
        perf_types=["blitz"]
    )

    if not pgn_content.strip():
        print("\n[!] Nenhum jogo novo encontrado!")
        print(">> Verificando se há mudanças para commitar...")
    else:
        # Salva os jogos organizados por categoria
        print("\n>> Salvando jogos...")
        stats = downloader.save_games_by_category(
            pgn_content,
            categorize=True
        )

        # Mostra estatísticas
        print("\n" + "="*60)
        print("[OK] DOWNLOAD CONCLUIDO!")
        print("="*60)
        print(f"Diretorio: {downloader.output_dir}/")
        print("\nEstatisticas:")
        total = 0
        for category, count in sorted(stats.items()):
            print(f"  {category}: {count} jogos")
            total += count
        print(f"\nTotal processado: {total} jogos")
        print("="*60)

    # Busca e salva estatísticas do perfil (sempre, mesmo sem jogos novos)
    print("\n>> Gerando arquivo de estatisticas...")
    try:
        user_stats = downloader.get_user_stats()
        stats_file = downloader.output_dir / "STATS.md"
        downloader.create_stats_markdown(user_stats, stats_file)
        print(f"[OK] Estatisticas salvas em: {stats_file}")
    except Exception as e:
        print(f"[!] Erro ao gerar estatisticas: {str(e)}")

    # Git operations
    print("\n>> Iniciando operacoes Git...")

    # Add all changes
    print("   - Adicionando arquivos ao Git...")
    subprocess.run(["git", "add", "pgn_games/"], check=True)

    # Check if there are changes
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True
    )

    if not result.stdout.strip():
        print("\n[!] Nenhuma mudanca para commitar")
        print("   Todos os jogos ja estao no repositorio")
        sys.exit(0)

    # Commit
    commit_msg = f"chore: update chess games - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    print(f"   - Criando commit: {commit_msg}")
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    # Push
    print("   - Enviando para repositorio remoto...")
    subprocess.run(["git", "push"], check=True)

    print("\n" + "="*60)
    print("[OK] GIT PUSH CONCLUIDO!")
    print("="*60)
    print(f"Commit: {commit_msg}")
    print("="*60 + "\n")

except subprocess.CalledProcessError as e:
    print(f"\n[ERRO] Falha no Git: {str(e)}")
    print("Verifique se o repositorio esta configurado corretamente")
    sys.exit(1)
except Exception as e:
    print(f"\n[ERRO] Falha na execucao: {str(e)}")
    sys.exit(1)
