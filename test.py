#!/usr/bin/env python3
"""
Teste rápido do Lichess Downloader
"""

from lichess_downloader import LichessDownloader
from datetime import datetime, timedelta

def test_download():
    """Testa o download de jogos."""

    # Solicita o username
    username = input("\n♟️  Digite seu nome de usuário do Lichess: ").strip()

    if not username:
        print("❌ Nome de usuário é obrigatório!")
        return

    print(f"\n🚀 Testando download para o usuário: {username}")
    print("📥 Buscando últimos 5 jogos...\n")

    try:
        # Cria o downloader
        downloader = LichessDownloader(username, output_dir="test_pgns")

        # Baixa apenas 5 jogos para teste
        pgn_content = downloader.download_games(max_games=5)

        if not pgn_content.strip():
            print("\n⚠️  Nenhum jogo encontrado.")
            print("Verifique se o nome de usuário está correto e se há jogos públicos.")
            return

        # Conta quantos jogos foram baixados
        games = downloader.parse_pgn_games(pgn_content)
        print(f"✅ {len(games)} jogos encontrados!\n")

        # Mostra informações do primeiro jogo
        if games:
            first_game = games[0]
            headers = first_game['headers']
            print("📋 Exemplo do primeiro jogo:")
            print(f"   Data: {headers.get('UTCDate', 'N/A')}")
            print(f"   Evento: {headers.get('Event', 'N/A')}")
            print(f"   Brancas: {headers.get('White', 'N/A')}")
            print(f"   Pretas: {headers.get('Black', 'N/A')}")
            print(f"   Resultado: {headers.get('Result', 'N/A')}")
            print(f"   Link: {headers.get('Site', 'N/A')}")

        # Salva os jogos organizados
        print(f"\n💾 Salvando jogos em: test_pgns/")
        stats = downloader.save_games_by_category(pgn_content, categorize=True)

        print("\n📊 Estatísticas:")
        for category, count in sorted(stats.items()):
            print(f"   {category}: {count} jogo(s)")

        print(f"\n✅ Teste concluído com sucesso!")
        print(f"📁 Jogos salvos em: {downloader.output_dir.absolute()}/")

    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        if "404" in str(e):
            print("💡 Dica: Verifique se o nome de usuário está correto.")
        elif "connection" in str(e).lower():
            print("💡 Dica: Verifique sua conexão com a internet.")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🧪 TESTE DO LICHESS PGN DOWNLOADER")
    print("="*60)
    test_download()
    print("\n")
