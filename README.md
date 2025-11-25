# Saboteur Engine

Biblioteca Python que implementa a lógica do jogo de tabuleiro Saboteur.
Desenvolvido como projeto acadêmico de Software Open Source.

## Instalação

```bash
pip install -i https://test.pypi.org/simple/ saboteur-engine-victor

from saboteur import SaboteurGame

# Iniciar jogo com 3 jogadores
jogo = SaboteurGame(["Ana", "Bob", "Carlos"])

# Jogar uma carta
# Jogador 0, usa a carta da posição 0 da mão, na coordenada x=1, y=0
resultado = jogo.jogar_turno(0, 0, 1, 0)
print(resultado)