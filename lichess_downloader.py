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
