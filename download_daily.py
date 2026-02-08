#!/usr/bin/env python3
"""
Script automático para baixar jogos diariamente
Baixa jogos a partir de 01/08/2025
"""

from datetime import datetime
from lichess_downloader import LichessDownloader
import sys

# Configurações
USERNAME = "r4v1"
START_DATE = datetime(2025, 8, 1)  # 01/08/2025

# Calcula o timestamp da data inicial
since = int(START_DATE.timestamp() * 1000)

print("="*60)
print("  LICHESS DAILY UPDATE")
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
        sys.exit(0)

    # Salva os jogos organizados por categoria
    print("\n>> Salvando jogos...")
    stats = downloader.save_games_by_category(
        pgn_content,
        categorize=True
    )

    # Mostra estatísticas
    print("\n" + "="*60)
    print("[OK] ATUALIZACAO CONCLUIDA!")
    print("="*60)
    print(f"Diretorio: {downloader.output_dir}/")
    print("\nEstatisticas:")
    total = 0
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} jogos")
        total += count
    print(f"\nTotal processado: {total} jogos")
    print("="*60)
    print(f"\nJogos salvos em: {downloader.output_dir.absolute()}\n")

except Exception as e:
    print(f"\n[ERRO] Falha na execucao: {str(e)}")
    sys.exit(1)
