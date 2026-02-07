#!/usr/bin/env python3
"""
Lichess PGN Downloader - CLI Interativa
Script principal para baixar e organizar jogos do Lichess.
"""

import sys
from datetime import datetime, timedelta
from lichess_downloader import LichessDownloader, timestamp_from_date


def print_header():
    """Imprime o cabeçalho da aplicação."""
    print("\n" + "="*60)
    print("  LICHESS PGN DOWNLOADER")
    print("  Baixe e organize seus jogos do Lichess")
    print("="*60 + "\n")


def get_username() -> str:
    """Solicita o nome de usuário do Lichess."""
    while True:
        username = input("Digite seu nome de usuário do Lichess: ").strip()
        if username:
            return username
        print("❌ Nome de usuário não pode ser vazio!")


def get_date_range() -> tuple:
    """
    Solicita a faixa de datas para download.

    Returns:
        Tupla (since_timestamp, until_timestamp)
    """
    print("\n📅 Faixa de tempo para download:")
    print("1. Últimos 7 dias")
    print("2. Último mês")
    print("3. Últimos 3 meses")
    print("4. Último ano")
    print("5. Todos os jogos")
    print("6. Período personalizado")

    choice = input("\nEscolha uma opção (1-6): ").strip()

    now = datetime.now()

    if choice == "1":
        since = int((now - timedelta(days=7)).timestamp() * 1000)
        return since, None
    elif choice == "2":
        since = int((now - timedelta(days=30)).timestamp() * 1000)
        return since, None
    elif choice == "3":
        since = int((now - timedelta(days=90)).timestamp() * 1000)
        return since, None
    elif choice == "4":
        since = int((now - timedelta(days=365)).timestamp() * 1000)
        return since, None
    elif choice == "5":
        return None, None
    elif choice == "6":
        print("\nFormato de data: YYYY-MM-DD (ex: 2024-01-01)")
        since_str = input("Data inicial (ou Enter para sem limite): ").strip()
        until_str = input("Data final (ou Enter para sem limite): ").strip()

        since = timestamp_from_date(since_str) if since_str else None
        until = timestamp_from_date(until_str) if until_str else None

        return since, until
    else:
        print("⚠️  Opção inválida, usando 'Todos os jogos'")
        return None, None


def get_game_types() -> list:
    """
    Solicita os tipos de jogos para download.

    Returns:
        Lista de tipos de jogo selecionados
    """
    print("\n♟️  Tipos de jogo:")
    print("1. Bullet (< 3 minutos)")
    print("2. Blitz (3-8 minutos)")
    print("3. Rapid (8-25 minutos)")
    print("4. Classical (> 25 minutos)")
    print("5. Correspondence (por correspondência)")
    print("6. Todos os tipos")

    types_map = {
        "1": ["bullet"],
        "2": ["blitz"],
        "3": ["rapid"],
        "4": ["classical"],
        "5": ["correspondence"],
        "6": None
    }

    choice = input("\nEscolha uma ou mais opções separadas por vírgula (ex: 1,2,3): ").strip()

    if "6" in choice:
        return None

    selected = []
    for c in choice.split(","):
        c = c.strip()
        if c in types_map and types_map[c]:
            selected.extend(types_map[c])

    return selected if selected else None


def get_color_filter() -> str:
    """
    Solicita filtro de cor.

    Returns:
        'white', 'black' ou None
    """
    print("\n🎨 Filtrar por cor:")
    print("1. Apenas jogos com brancas")
    print("2. Apenas jogos com pretas")
    print("3. Ambas as cores")

    choice = input("\nEscolha uma opção (1-3): ").strip()

    if choice == "1":
        return "white"
    elif choice == "2":
        return "black"
    else:
        return None


def get_result_filter() -> str:
    """
    Solicita filtro de resultado.

    Returns:
        'win', 'loss', 'draw' ou None
    """
    print("\n🏆 Filtrar por resultado:")
    print("1. Apenas vitórias")
    print("2. Apenas derrotas")
    print("3. Apenas empates")
    print("4. Todos os resultados")

    choice = input("\nEscolha uma opção (1-4): ").strip()

    if choice == "1":
        return "win"
    elif choice == "2":
        return "loss"
    elif choice == "3":
        return "draw"
    else:
        return None


def get_max_games() -> int:
    """
    Solicita número máximo de jogos.

    Returns:
        Número máximo de jogos ou None para sem limite
    """
    print("\n🔢 Número máximo de jogos:")
    max_input = input("Digite o número máximo (ou Enter para sem limite): ").strip()

    if max_input.isdigit():
        return int(max_input)
    return None


def confirm_download(params: dict) -> bool:
    """
    Mostra resumo e solicita confirmação.

    Args:
        params: Dicionário com parâmetros do download

    Returns:
        True se confirmado, False caso contrário
    """
    print("\n" + "="*60)
    print("📋 RESUMO DO DOWNLOAD")
    print("="*60)
    print(f"Usuário: {params['username']}")
    print(f"Período: {params['date_range']}")
    print(f"Tipos de jogo: {params['game_types']}")
    print(f"Cor: {params['color']}")
    print(f"Resultado: {params['result']}")
    print(f"Máximo de jogos: {params['max_games']}")
    print(f"Organizar por categoria: {params['categorize']}")
    print("="*60)

    confirm = input("\n✅ Confirmar download? (s/n): ").strip().lower()
    return confirm in ['s', 'sim', 'y', 'yes']


def main():
    """Função principal - CLI interativa."""
    try:
        print_header()

        # Coleta informações do usuário
        username = get_username()
        since, until = get_date_range()
        game_types = get_game_types()
        color = get_color_filter()
        result = get_result_filter()
        max_games = get_max_games()

        # Pergunta sobre categorização
        categorize_input = input("\n📁 Organizar jogos em pastas por categoria? (s/n): ").strip().lower()
        categorize = categorize_input in ['s', 'sim', 'y', 'yes']

        # Prepara resumo
        params = {
            'username': username,
            'date_range': f"Desde {datetime.fromtimestamp(since/1000).strftime('%Y-%m-%d') if since else 'início'} até {datetime.fromtimestamp(until/1000).strftime('%Y-%m-%d') if until else 'agora'}",
            'game_types': ', '.join(game_types) if game_types else 'Todos',
            'color': color if color else 'Ambas',
            'result': result if result else 'Todos',
            'max_games': max_games if max_games else 'Sem limite',
            'categorize': 'Sim' if categorize else 'Não'
        }

        # Confirmação
        if not confirm_download(params):
            print("\n❌ Download cancelado.")
            return

        # Inicia download
        print("\n🚀 Iniciando download...")
        downloader = LichessDownloader(username)

        pgn_content = downloader.download_games(
            since=since,
            until=until,
            max_games=max_games,
            perf_types=game_types,
            color=color
        )

        if not pgn_content.strip():
            print("\n⚠️  Nenhum jogo encontrado com os filtros especificados.")
            return

        # Salva os jogos
        print("💾 Salvando jogos...")
        stats = downloader.save_games_by_category(
            pgn_content,
            categorize=categorize,
            result_filter=result
        )

        # Mostra estatísticas
        print("\n" + "="*60)
        print("✅ DOWNLOAD CONCLUÍDO!")
        print("="*60)
        print(f"Jogos salvos em: {downloader.output_dir}/")
        print("\nEstatísticas:")
        for category, count in sorted(stats.items()):
            print(f"  {category}: {count} jogos")
        print("="*60)

        print("\n💡 Dica: Você pode agora analisar esses jogos com Claude ou outras IAs!")
        print(f"📂 Os jogos estão em: {downloader.output_dir.absolute()}\n")

    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
