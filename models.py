from dataclasses import dataclass
from typing import Tuple, Optional

# Representação de conexões: (Cima, Direita, Baixo, Esquerda)
# 1 = Aberto (Cano), 0 = Fechado (Parede)
CONEXAO_HORIZONTAL = (0, 1, 0, 1)
CONEXAO_VERTICAL = (1, 0, 1, 0)
CONEXAO_CRUZ = (1, 1, 1, 1)

@dataclass
class Carta:
    """Representa uma carta do jogo."""
    id: str
    nome: str
    tipo: str  # 'caminho' ou 'acao'
    conexoes: Optional[Tuple[int, int, int, int]] = None
    
    def __repr__(self):
        return f"[{self.nome}]"

class Jogador:
    """Representa um jogador."""
    def __init__(self, nome: str, papel: str):
        self.nome = nome
        self.papel = papel  # 'Anao' ou 'Sabotador'
        self.mao = []  

    def comprar_carta(self, carta: Carta):
        self.mao.append(carta)

    def jogar_carta(self, index_carta: int):
        if 0 <= index_carta < len(self.mao):
            return self.mao.pop(index_carta)
        return None