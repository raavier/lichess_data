# Lichess PGN Downloader

Ferramenta Python para baixar e organizar seus jogos do Lichess em formato PGN, facilitando análises posteriores com IAs como Claude.

## Características

- **Download via API do Lichess**: Utiliza a API oficial do Lichess para baixar seus jogos
- **Filtros avançados**:
  - Faixa de tempo (data início/fim)
  - Tipo de jogo (Bullet, Blitz, Rapid, Classical, Correspondence)
  - Cor das peças (brancas/pretas)
  - Resultado (vitória/derrota/empate)
  - Limite de número de jogos
- **Organização automática**: Separa os jogos em pastas por categoria
- **Interface interativa**: CLI amigável que guia você através das opções
- **Pronto para análise**: Formato PGN compatível com análise por IA

## Instalação

1. Clone este repositório:
```bash
git clone <seu-repositorio>
cd lichess_data
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Modo Interativo (Recomendado)

Execute o script principal e siga as instruções:

```bash
python main.py
```

A CLI irá guiá-lo através das seguintes opções:

1. **Nome de usuário** do Lichess
2. **Faixa de tempo**:
   - Últimos 7 dias
   - Último mês
   - Últimos 3 meses
   - Último ano
   - Todos os jogos
   - Período personalizado
3. **Tipos de jogo**:
   - Bullet (< 3 minutos)
   - Blitz (3-8 minutos)
   - Rapid (8-25 minutos)
   - Classical (> 25 minutos)
   - Correspondence
   - Todos
4. **Filtro de cor**: brancas, pretas ou ambas
5. **Filtro de resultado**: vitórias, derrotas, empates ou todos
6. **Número máximo de jogos**: limite opcional
7. **Organização**: se deseja separar em pastas por categoria

### Modo Programático

Você também pode usar a biblioteca diretamente em seus scripts:

```python
from lichess_downloader import LichessDownloader
from datetime import datetime, timedelta

# Cria o downloader
downloader = LichessDownloader("seu_username")

# Download dos últimos 30 dias
since = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)

pgn_content = downloader.download_games(
    since=since,
    perf_types=["blitz", "rapid"],
    max_games=100
)

# Salva organizando por categoria
stats = downloader.save_games_by_category(
    pgn_content,
    categorize=True,
    result_filter="win"
)

print(f"Jogos salvos: {stats}")
```

## Estrutura de Diretórios

Quando a categorização está ativada, os jogos são organizados assim:

```
pgn_games/
├── bullet/
│   ├── 2024-01-15_14-30-00_opponent1.pgn
│   └── 2024-01-16_10-15-00_opponent2.pgn
├── blitz/
│   ├── 2024-01-15_16-00-00_opponent3.pgn
│   └── 2024-01-17_20-45-00_opponent4.pgn
├── rapid/
│   └── 2024-01-18_18-30-00_opponent5.pgn
├── classical/
└── correspondence/
```

Cada arquivo PGN contém um jogo completo com:
- Metadados (jogadores, data, resultado, rating, etc.)
- Movimentos em notação algébrica
- Informações de tempo
- Abertura utilizada

## Analisando com Claude

Após baixar seus jogos, você pode analisá-los com Claude de várias formas:

### 1. Análise Individual

```
"Analise este jogo e me dê feedback sobre meus erros:"
[Cole o conteúdo de um arquivo .pgn]
```

### 2. Análise de Padrões

```
"Tenho 50 jogos de blitz na pasta pgn_games/blitz/.
Analise os padrões de erros mais comuns que cometo."
```

### 3. Análise de Aberturas

```
"Analise minhas aberturas mais jogadas e sugira melhorias."
```

### 4. Estatísticas Personalizadas

```
"Calcule minha taxa de vitória por tipo de jogo e abertura."
```

## API do Lichess

Esta ferramenta usa a API pública do Lichess:
- **Endpoint**: `https://lichess.org/api/games/user/{username}`
- **Documentação**: https://lichess.org/api
- **Limite de taxa**: A API do Lichess é generosa, mas evite fazer muitas requisições em sequência
- **Sem autenticação necessária**: Para jogos públicos, não é necessário token de API

## Tipos de Jogo (Lichess)

- **Bullet**: Menos de 3 minutos total
- **Blitz**: 3 a 8 minutos total
- **Rapid**: 8 a 25 minutos total
- **Classical**: 25+ minutos total
- **Correspondence**: Jogos por correspondência (vários dias)

## Formato PGN

PGN (Portable Game Notation) é o formato padrão para representar jogos de xadrez. Cada arquivo contém:

```pgn
[Event "Rated Blitz game"]
[Site "https://lichess.org/abc123"]
[Date "2024.01.15"]
[White "player1"]
[Black "player2"]
[Result "1-0"]
[WhiteElo "1500"]
[BlackElo "1480"]
[TimeControl "180+0"]
[Opening "Sicilian Defense"]

1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 ...
```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## Licença

MIT License

## Avisos

- Esta ferramenta baixa apenas **jogos públicos**
- Respeite os termos de uso do Lichess
- Use com moderação para não sobrecarregar a API
- Os PGNs são salvos localmente - faça backup se necessário

## Próximos Passos

Sugestões de melhorias futuras:
- [ ] Adicionar análise de engine (Stockfish)
- [ ] Gerar relatórios HTML com estatísticas
- [ ] Exportar para outros formatos (JSON, CSV)
- [ ] Interface web
- [ ] Comparação entre períodos
- [ ] Integração com Chess.com

## Suporte

Se encontrar problemas ou tiver dúvidas:
1. Verifique se suas dependências estão instaladas
2. Confirme que seu nome de usuário do Lichess está correto
3. Verifique sua conexão com a internet
4. Consulte a documentação da API do Lichess

---

Feito com ♟️ para melhorar no xadrez através de análise com IA
