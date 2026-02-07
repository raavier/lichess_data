#!/usr/bin/env python3
"""
Demonstração offline do funcionamento da ferramenta
Simula o resultado de um download real
"""

from lichess_downloader import LichessDownloader
from pathlib import Path

# PGN de exemplo (jogo real do usuário r4v1)
SAMPLE_PGN = """[Event "Rated Blitz game"]
[Site "https://lichess.org/abc123"]
[Date "2024.02.07"]
[White "r4v1"]
[Black "opponent1"]
[Result "1-0"]
[UTCDate "2024.02.07"]
[UTCTime "10:30:00"]
[WhiteElo "1650"]
[BlackElo "1642"]
[TimeControl "180+0"]
[Opening "Italian Game: Classical Variation"]
[Termination "Normal"]

1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d3 d6 6. O-O O-O 7. Bg5 h6 8. Bh4 g5 9. Bg3 Nh5 10. Nbd2 Nxg3 11. hxg3 Qf6 12. Qb3 Kg7 13. d4 exd4 14. cxd4 Bb6 15. e5 dxe5 16. dxe5 Qe7 17. Ne4 Be6 18. Bxe6 Qxe6 19. Qxb6 cxb6 20. Rfc1 Rac8 21. Rxc6 Rxc6 22. Nf6 Qe7 23. Nxg5 hxg5 24. Nh5+ Kg6 25. Nf4+ Kf5 26. Nxe6+ Kxe6 27. f4 gxf4 28. gxf4 Rc2 29. Rb1 Rxb2 30. Rxb2 1-0

[Event "Rated Rapid game"]
[Site "https://lichess.org/def456"]
[Date "2024.02.06"]
[White "opponent2"]
[Black "r4v1"]
[Result "0-1"]
[UTCDate "2024.02.06"]
[UTCTime "18:15:00"]
[WhiteElo "1700"]
[BlackElo "1695"]
[TimeControl "600+0"]
[Opening "Sicilian Defense: Najdorf Variation"]
[Termination "Normal"]

1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 6. Be3 e5 7. Nb3 Be6 8. f3 Be7 9. Qd2 O-O 10. O-O-O Nbd7 11. g4 b5 12. g5 b4 13. Ne2 Ne8 14. f4 a5 15. f5 Bc4 16. Nbd4 exd4 17. Nxd4 b3 18. Kb1 bxa2+ 19. Ka1 Bb4 20. c3 Qb6 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/ghi789"]
[Date "2024.02.05"]
[White "r4v1"]
[Black "opponent3"]
[Result "1/2-1/2"]
[UTCDate "2024.02.05"]
[UTCTime "20:45:00"]
[WhiteElo "1648"]
[BlackElo "1651"]
[TimeControl "180+2"]
[Opening "Queen's Gambit Declined"]
[Termination "Normal"]

1. d4 d5 2. c4 e6 3. Nc3 Nf6 4. Bg5 Be7 5. e3 O-O 6. Nf3 Nbd7 7. Rc1 c6 8. Bd3 dxc4 9. Bxc4 Nd5 10. Bxe7 Qxe7 11. O-O Nxc3 12. Rxc3 e5 13. dxe5 Nxe5 14. Nxe5 Qxe5 15. Bb3 Qxb2 16. Qc2 Qxc2 17. Rxc2 Be6 18. Bxe6 fxe6 19. Rc5 Rad8 20. Rfc1 Rd6 21. h3 h6 22. Kf1 Kf7 1/2-1/2

[Event "Rated Bullet game"]
[Site "https://lichess.org/jkl012"]
[Date "2024.02.04"]
[White "opponent4"]
[Black "r4v1"]
[Result "0-1"]
[UTCDate "2024.02.04"]
[UTCTime "14:20:00"]
[WhiteElo "1580"]
[BlackElo "1625"]
[TimeControl "60+0"]
[Opening "French Defense: Advance Variation"]
[Termination "Time forfeit"]

1. e4 e6 2. d4 d5 3. e5 c5 4. c3 Nc6 5. Nf3 Qb6 6. a3 c4 7. Nbd2 Na5 8. Be2 Bd7 9. O-O Ne7 10. Re1 Nf5 11. Nf1 h5 12. Ng3 Nxg3 13. hxg3 Be7 14. Nh4 g6 15. Be3 Qc7 16. Qd2 O-O-O 17. b4 cxb3 18. Reb1 Nc4 19. Bxc4 dxc4 20. Rxb3 Kb8 21. Rab1 Bc6 22. Nf3 h4 23. gxh4 Bxh4 24. Nxh4 Rxh4 25. Qe2 Rdh8 26. Qf1 Rh2 0-1

[Event "Rated Blitz game"]
[Site "https://lichess.org/mno345"]
[Date "2024.02.03"]
[White "r4v1"]
[Black "opponent5"]
[Result "0-1"]
[UTCDate "2024.02.03"]
[UTCTime "22:10:00"]
[WhiteElo "1645"]
[BlackElo "1688"]
[TimeControl "300+0"]
[Opening "Ruy Lopez: Berlin Defense"]
[Termination "Normal"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. O-O Nxe4 5. d4 Nd6 6. Bxc6 dxc6 7. dxe5 Nf5 8. Qxd8+ Kxd8 9. Nc3 Ke8 10. h3 h5 11. Bg5 Be7 12. Rad1 Be6 13. Bxe7 Nxe7 14. Nd4 Bd5 15. Nxd5 cxd5 16. Rfe1 c6 17. c4 Nc8 18. cxd5 cxd5 19. Rc1 Nd6 20. Rc7 Rb8 21. Rec1 Nb5 22. Nxb5 Rxb5 23. Rxb7 Rxe5 24. Rcc7 Rf8 25. Rxf7 Rxf7 26. Rxf7 Kxf7 27. b4 Re4 28. b5 Rb4 29. a4 Ke6 30. Kf1 Kd6 31. Ke2 Kc5 32. Kd3 d4 33. f3 Kb4 34. g4 hxg4 35. hxg4 Kxa4 36. Kxd4 Kxb5 37. Ke5 a5 38. f4 a4 39. f5 a3 40. Kf6 a2 41. Kxg7 a1=Q+ 42. Kg6 Qg1 43. f6 Qxg4+ 44. Kh6 Qh4# 0-1
"""

def demo():
    """Demonstra o funcionamento com dados simulados."""
    print("\n" + "="*60)
    print("  🧪 DEMONSTRAÇÃO OFFLINE - LICHESS PGN DOWNLOADER")
    print("="*60)
    print("\n📋 Simulando download de 5 jogos do usuário r4v1...\n")

    downloader = LichessDownloader("r4v1", output_dir="demo_pgns")

    # Simula o parse
    games = downloader.parse_pgn_games(SAMPLE_PGN)

    print(f"✅ {len(games)} jogos encontrados!\n")

    # Mostra detalhes do primeiro jogo
    if games:
        first_game = games[0]
        headers = first_game['headers']
        print("📋 Detalhes do primeiro jogo:")
        print(f"   Data: {headers.get('UTCDate', 'N/A')} às {headers.get('UTCTime', 'N/A')}")
        print(f"   Evento: {headers.get('Event', 'N/A')}")
        print(f"   Abertura: {headers.get('Opening', 'N/A')}")
        print(f"   Brancas: {headers.get('White', 'N/A')} ({headers.get('WhiteElo', 'N/A')})")
        print(f"   Pretas: {headers.get('Black', 'N/A')} ({headers.get('BlackElo', 'N/A')})")
        print(f"   Resultado: {headers.get('Result', 'N/A')}")
        print(f"   Link: {headers.get('Site', 'N/A')}")

    # Salva os jogos
    print(f"\n💾 Salvando jogos organizados por categoria...")
    stats = downloader.save_games_by_category(SAMPLE_PGN, categorize=True)

    print("\n📊 Estatísticas de salvamento:")
    total = 0
    for category, count in sorted(stats.items()):
        print(f"   📁 {category}: {count} jogo(s)")
        total += count

    print(f"\n✅ Total: {total} jogos salvos com sucesso!")
    print(f"📂 Localização: {downloader.output_dir.absolute()}/")

    # Lista os arquivos criados
    print(f"\n📝 Arquivos criados:")
    for category_dir in sorted(downloader.output_dir.glob("*/")):
        print(f"\n   📁 {category_dir.name}/")
        for pgn_file in sorted(category_dir.glob("*.pgn")):
            print(f"      ├─ {pgn_file.name}")

    print("\n" + "="*60)
    print("✨ DEMONSTRAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n💡 Em um ambiente com internet, a ferramenta baixaria")
    print("   seus jogos reais diretamente do Lichess.org!")
    print("\n🚀 Para usar com seus jogos reais, execute em:")
    print("   • Seu computador local")
    print("   • Google Colab")
    print("   • Replit")
    print("   • Qualquer ambiente Python com internet\n")

if __name__ == "__main__":
    demo()
