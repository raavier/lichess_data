#!/usr/bin/env python3
"""
Script para baixar jogos do usuário r4v1
Últimos 6 meses, apenas Blitz
"""

from datetime import datetime, timedelta
from lichess_downloader import LichessDownloader

# Configurações
USERNAME = "r4v1"
MONTHS = 6

# Calcula o timestamp de 6 meses atrás
since = int((datetime.now() - timedelta(days=30 * MONTHS)).timestamp() * 1000)

print("="*60)
print("  BAIXANDO JOGOS DO LICHESS")
print("="*60)
print(f"Usuário: {USERNAME}")
print(f"Período: Últimos {MONTHS} meses")
print(f"Tipo: Blitz")
print("="*60)

# Cria o downloader
downloader = LichessDownloader(USERNAME)

# Baixa os jogos
print("\n>> Iniciando download...")
pgn_content = downloader.download_games(
    since=since,
    perf_types=["blitz"]
)

if not pgn_content.strip():
    print("\n[!] Nenhum jogo encontrado!")
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
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} jogos")
    print("="*60)
    print(f"\nJogos salvos em: {downloader.output_dir.absolute()}\n")
