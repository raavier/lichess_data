#!/usr/bin/env python3
"""
Exemplo de uso da biblioteca Lichess Downloader
Este arquivo demonstra como usar a biblioteca programaticamente.
"""

from lichess_downloader import LichessDownloader
from datetime import datetime, timedelta


def example_basic():
    """Exemplo básico: baixar todos os jogos."""
    print("=== Exemplo 1: Download Básico ===\n")

    downloader = LichessDownloader("seu_username_aqui")

    # Baixa todos os jogos (cuidado: pode ser muitos!)
    pgn_content = downloader.download_games(max_games=10)

    # Salva sem categorizar
    stats = downloader.save_games_by_category(pgn_content, categorize=False)

    print(f"Jogos baixados: {sum(stats.values())}")
    print(f"Salvos em: {downloader.output_dir}/\n")


def example_filtered():
    """Exemplo com filtros: apenas jogos blitz do último mês."""
    print("=== Exemplo 2: Download com Filtros ===\n")

    downloader = LichessDownloader("seu_username_aqui")

    # Últimos 30 dias
    since = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)

    # Apenas jogos blitz
    pgn_content = downloader.download_games(
        since=since,
        perf_types=["blitz"],
        max_games=50
    )

    # Salva organizando por categoria
    stats = downloader.save_games_by_category(pgn_content, categorize=True)

    print("Estatísticas:")
    for category, count in stats.items():
        print(f"  {category}: {count} jogos")
    print()


def example_wins_only():
    """Exemplo: apenas vitórias dos últimos 3 meses."""
    print("=== Exemplo 3: Apenas Vitórias ===\n")

    downloader = LichessDownloader("seu_username_aqui")

    # Últimos 90 dias
    since = int((datetime.now() - timedelta(days=90)).timestamp() * 1000)

    # Baixa jogos
    pgn_content = downloader.download_games(
        since=since,
        perf_types=["rapid", "blitz"],
        max_games=100
    )

    # Salva apenas vitórias
    stats = downloader.save_games_by_category(
        pgn_content,
        categorize=True,
        result_filter="win"
    )

    print(f"Vitórias salvas: {sum(stats.values())}")
    print("Por categoria:")
    for category, count in stats.items():
        print(f"  {category}: {count} vitórias")
    print()


def example_white_pieces():
    """Exemplo: jogos com brancas apenas."""
    print("=== Exemplo 4: Apenas Jogos com Brancas ===\n")

    downloader = LichessDownloader("seu_username_aqui")

    # Apenas jogos onde você jogou com brancas
    pgn_content = downloader.download_games(
        color="white",
        perf_types=["blitz"],
        max_games=30
    )

    stats = downloader.save_games_by_category(pgn_content, categorize=True)

    print(f"Jogos com brancas: {sum(stats.values())}\n")


def example_custom_period():
    """Exemplo: período personalizado."""
    print("=== Exemplo 5: Período Personalizado ===\n")

    downloader = LichessDownloader("seu_username_aqui")

    # De 1 de janeiro de 2024 até 31 de março de 2024
    since = int(datetime(2024, 1, 1).timestamp() * 1000)
    until = int(datetime(2024, 3, 31).timestamp() * 1000)

    pgn_content = downloader.download_games(
        since=since,
        until=until,
        max_games=200
    )

    stats = downloader.save_games_by_category(pgn_content, categorize=True)

    print("Jogos do período:")
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} jogos")
    print()


def example_analysis_ready():
    """Exemplo: preparar jogos para análise com Claude."""
    print("=== Exemplo 6: Preparar para Análise com Claude ===\n")

    downloader = LichessDownloader("seu_username_aqui", output_dir="games_for_analysis")

    # Últimas 2 semanas, apenas derrotas (para aprender com erros)
    since = int((datetime.now() - timedelta(days=14)).timestamp() * 1000)

    pgn_content = downloader.download_games(
        since=since,
        perf_types=["blitz", "rapid"],
        max_games=20
    )

    # Salva apenas derrotas, organizadas por categoria
    stats = downloader.save_games_by_category(
        pgn_content,
        categorize=True,
        result_filter="loss"
    )

    print("🎯 Jogos prontos para análise:")
    print(f"📁 Localização: {downloader.output_dir}/")
    print(f"📊 Total de derrotas para analisar: {sum(stats.values())}")
    print("\n💡 Próximo passo:")
    print("   Envie esses PGNs para Claude e peça análise de erros comuns!\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  EXEMPLOS DE USO - LICHESS PGN DOWNLOADER")
    print("="*60 + "\n")

    print("⚠️  ANTES DE EXECUTAR:")
    print("   1. Substitua 'seu_username_aqui' pelo seu nome de usuário do Lichess")
    print("   2. Descomente o exemplo que deseja testar")
    print("   3. Execute: python example.py\n")

    print("="*60 + "\n")

    # Descomente o exemplo que deseja executar:

    # example_basic()
    # example_filtered()
    # example_wins_only()
    # example_white_pieces()
    # example_custom_period()
    # example_analysis_ready()

    print("✅ Veja mais exemplos no código deste arquivo!")
    print("📖 Consulte o README.md para documentação completa.\n")
