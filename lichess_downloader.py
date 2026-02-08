"""
Lichess PGN Downloader
Ferramenta para baixar e organizar jogos do Lichess em formato PGN.
"""

import requests
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from dateutil import parser as date_parser


class LichessDownloader:
    """Cliente para download de jogos do Lichess via API."""

    BASE_URL = "https://lichess.org/api"

    def __init__(self, username: str, output_dir: str = "pgn_games"):
        """
        Inicializa o downloader.

        Args:
            username: Nome de usuário do Lichess
            output_dir: Diretório para salvar os PGNs
        """
        self.username = username
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def get_user_stats(self) -> Dict:
        """
        Busca estatísticas do perfil do usuário no Lichess.

        Returns:
            Dicionário com as estatísticas do usuário
        """
        url = f"{self.BASE_URL}/user/{self.username}"

        headers = {
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    def create_stats_markdown(self, stats: Dict, filepath: Optional[str] = None) -> str:
        """
        Cria um arquivo markdown com as estatísticas do usuário.

        Args:
            stats: Dicionário com estatísticas do usuário
            filepath: Caminho para salvar o arquivo (opcional)

        Returns:
            Conteúdo markdown gerado
        """
        perfs = stats.get('perfs', {})
        count = stats.get('count', {})
        play_time = stats.get('playTime', {})
        created_at = stats.get('createdAt', 0)
        seen_at = stats.get('seenAt', 0)

        # Converte timestamps para datas legíveis
        created_date = datetime.fromtimestamp(created_at / 1000).strftime('%d/%m/%Y')
        last_seen = datetime.fromtimestamp(seen_at / 1000).strftime('%d/%m/%Y %H:%M')

        # Calcula tempo total em horas
        total_hours = play_time.get('total', 0) / 3600 if play_time else 0

        # Constrói o conteúdo markdown
        md_content = f"""# Estatisticas Lichess - {self.username}

**Atualizado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## Informacoes Gerais

- **Usuario:** {self.username}
- **Perfil:** https://lichess.org/@/{self.username}
- **Conta criada:** {created_date}
- **Ultima atividade:** {last_seen}
- **Tempo total jogando:** {total_hours:.1f} horas

## Estatisticas de Partidas

- **Total de partidas:** {count.get('all', 0)}
- **Partidas ranqueadas:** {count.get('rated', 0)}
- **Vitorias:** {count.get('win', 0)} ({count.get('win', 0) / count.get('all', 1) * 100:.1f}%)
- **Derrotas:** {count.get('loss', 0)} ({count.get('loss', 0) / count.get('all', 1) * 100:.1f}%)
- **Empates:** {count.get('draw', 0)} ({count.get('draw', 0) / count.get('all', 1) * 100:.1f}%)

## Ratings por Modalidade

"""

        # Ordena modalidades por número de jogos
        game_modes = []
        for mode, data in perfs.items():
            if isinstance(data, dict) and 'rating' in data:
                games = data.get('games', 0)
                rating = data.get('rating', 0)
                rd = data.get('rd', 0)
                prov = data.get('prov', False)
                prog = data.get('prog', 0)

                game_modes.append({
                    'mode': mode,
                    'games': games,
                    'rating': rating,
                    'rd': rd,
                    'prov': prov,
                    'prog': prog
                })

        # Ordena por número de jogos (decrescente)
        game_modes.sort(key=lambda x: x['games'], reverse=True)

        # Adiciona cada modalidade
        for mode_data in game_modes:
            mode_name = mode_data['mode'].capitalize()
            rating = mode_data['rating']
            games = mode_data['games']
            prov = " (Provisorio)" if mode_data['prov'] else ""
            prog = mode_data['prog']
            prog_str = f" ({prog:+d})" if prog != 0 else ""

            md_content += f"### {mode_name}\n\n"
            md_content += f"- **Rating:** {rating}{prov}{prog_str}\n"
            md_content += f"- **Partidas:** {games}\n"
            md_content += f"- **RD (Rating Deviation):** {mode_data['rd']}\n\n"

        # Salva em arquivo se filepath for fornecido
        if filepath:
            filepath_obj = Path(filepath)
            filepath_obj.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath_obj, 'w', encoding='utf-8') as f:
                f.write(md_content)

        return md_content

    def download_games(
        self,
        since: Optional[int] = None,
        until: Optional[int] = None,
        max_games: Optional[int] = None,
        perf_types: Optional[List[str]] = None,
        color: Optional[str] = None,
        rated: Optional[bool] = None,
        ongoing: bool = False,
        finished: bool = True
    ) -> str:
        """
        Baixa jogos do usuário com filtros especificados.

        Args:
            since: Timestamp em ms - baixar jogos a partir desta data
            until: Timestamp em ms - baixar jogos até esta data
            max_games: Número máximo de jogos para baixar
            perf_types: Lista de tipos de jogo (blitz, bullet, rapid, classical, etc.)
            color: Filtrar por cor ('white' ou 'black')
            rated: Se True, apenas jogos ranqueados; se False, apenas casuais
            ongoing: Incluir jogos em andamento
            finished: Incluir jogos finalizados

        Returns:
            Conteúdo PGN dos jogos
        """
        url = f"{self.BASE_URL}/games/user/{self.username}"

        params = {
            "pgnInJson": "false",
            "clocks": "true",
            "evals": "false",
            "opening": "true",
            "ongoing": str(ongoing).lower(),
            "finished": str(finished).lower(),
        }

        if since:
            params["since"] = since
        if until:
            params["until"] = until
        if max_games:
            params["max"] = max_games
        if perf_types:
            params["perfType"] = ",".join(perf_types)
        if color:
            params["color"] = color
        if rated is not None:
            params["rated"] = str(rated).lower()

        headers = {
            "Accept": "application/x-chess-pgn"
        }

        print(f"Baixando jogos de {self.username}...")
        print(f"Parâmetros: {params}")

        response = requests.get(url, params=params, headers=headers, stream=True)
        response.raise_for_status()

        pgn_content = ""
        for chunk in response.iter_content(chunk_size=8192, decode_unicode=False):
            if chunk:
                pgn_content += chunk.decode('utf-8')

        return pgn_content

    def parse_pgn_games(self, pgn_content: str) -> List[Dict[str, str]]:
        """
        Separa o conteúdo PGN em jogos individuais.

        Args:
            pgn_content: Conteúdo PGN completo

        Returns:
            Lista de dicionários com informações de cada jogo
        """
        games = []
        current_game = []
        headers = {}
        in_moves = False

        for line in pgn_content.split('\n'):
            if line.startswith('['):
                # Se estamos começando headers e já temos um jogo, salva o anterior
                if current_game and in_moves:
                    games.append({
                        'pgn': '\n'.join(current_game),
                        'headers': headers.copy()
                    })
                    current_game = []
                    headers = {}
                    in_moves = False

                # Extrai cabeçalho
                match = re.match(r'\[(\w+)\s+"([^"]+)"\]', line)
                if match:
                    key, value = match.groups()
                    headers[key] = value
                current_game.append(line)
            elif line.strip() and not line.startswith('['):
                # Linha com conteúdo (movimentos)
                in_moves = True
                current_game.append(line)
            else:
                # Linha vazia
                current_game.append(line)

        # Adiciona o último jogo se existir
        if current_game and headers:
            games.append({
                'pgn': '\n'.join(current_game),
                'headers': headers.copy()
            })

        return games

    def categorize_game(self, game: Dict[str, str]) -> str:
        """
        Determina a categoria do jogo baseado nos headers.

        Args:
            game: Dicionário com informações do jogo

        Returns:
            Nome da categoria
        """
        headers = game['headers']

        # Extrai tipo de jogo (Event) - case insensitive
        event = headers.get('Event', 'Unknown').lower()

        if 'bullet' in event:
            return 'bullet'
        elif 'blitz' in event:
            return 'blitz'
        elif 'rapid' in event:
            return 'rapid'
        elif 'classical' in event:
            return 'classical'
        elif 'correspondence' in event:
            return 'correspondence'
        else:
            return 'other'

    def save_games_by_category(
        self,
        pgn_content: str,
        categorize: bool = True,
        result_filter: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Salva jogos organizados por categoria.

        Args:
            pgn_content: Conteúdo PGN completo
            categorize: Se True, organiza em subpastas por categoria
            result_filter: Filtrar por resultado ('win', 'loss', 'draw')

        Returns:
            Dicionário com estatísticas de salvamento
        """
        games = self.parse_pgn_games(pgn_content)
        stats = {}

        print(f"\nTotal de jogos encontrados: {len(games)}")

        for game in games:
            headers = game['headers']

            # Filtro por resultado
            if result_filter:
                result = headers.get('Result', '')
                player_color = 'White' if headers.get('White') == self.username else 'Black'

                if result_filter == 'win':
                    if (player_color == 'White' and result != '1-0') or \
                       (player_color == 'Black' and result != '0-1'):
                        continue
                elif result_filter == 'loss':
                    if (player_color == 'White' and result != '0-1') or \
                       (player_color == 'Black' and result != '1-0'):
                        continue
                elif result_filter == 'draw':
                    if result != '1/2-1/2':
                        continue

            # Determina pasta de destino
            if categorize:
                category = self.categorize_game(game)
                game_dir = self.output_dir / category
            else:
                game_dir = self.output_dir

            game_dir.mkdir(exist_ok=True)

            # Nome do arquivo baseado na data e adversário
            date_str = headers.get('UTCDate', 'unknown').replace('.', '-')
            time_str = headers.get('UTCTime', 'unknown').replace(':', '-')
            opponent = headers.get('Black') if headers.get('White') == self.username else headers.get('White', 'unknown')

            filename = f"{date_str}_{time_str}_{opponent}.pgn"
            filepath = game_dir / filename

            # Salva o jogo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(game['pgn'])

            # Atualiza estatísticas
            category_name = category if categorize else 'all'
            stats[category_name] = stats.get(category_name, 0) + 1

        return stats


def timestamp_from_date(date_str: str) -> int:
    """
    Converte uma string de data para timestamp em milissegundos.

    Args:
        date_str: Data em formato legível (ex: '2024-01-01', 'yesterday', '1 week ago')

    Returns:
        Timestamp em milissegundos
    """
    dt = date_parser.parse(date_str)
    return int(dt.timestamp() * 1000)
