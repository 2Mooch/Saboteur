import random
from collections import deque
from .models import Carta, Jogador, CONEXAO_HORIZONTAL, CONEXAO_VERTICAL, CONEXAO_CRUZ

class SaboteurGame:
    def __init__(self, nomes_jogadores: list):
        self.rodada = 0
        self.deck = self._criar_deck()
        self.jogadores = self._distribuir_papeis(nomes_jogadores)
        
        # O tabuleiro começa com a carta inicial no meio (0,0)
        start_card = Carta("start", "Inicio", "caminho", CONEXAO_CRUZ)
        self.tabuleiro = {(0, 0): start_card}
        
        # Objetivos ocultos
        self.objetivos = {(8, 0): "ouro", (8, -2): "carvao", (8, 2): "carvao"} 
        self.vencedor = None
        
        self._distribuir_mao_inicial()

    def _criar_deck(self):
        deck = []
        for _ in range(15):
            deck.append(Carta("path_h", "Tubo Horizontal", "caminho", CONEXAO_HORIZONTAL))
            deck.append(Carta("path_v", "Tubo Vertical", "caminho", CONEXAO_VERTICAL))
            deck.append(Carta("curve_rb", "Curva Dir-Baixo", "caminho", (0, 1, 1, 0)))
            deck.append(Carta("curve_rt", "Curva Dir-Cima", "caminho", (1, 1, 0, 0)))
        random.shuffle(deck)
        return deck

    def _distribuir_papeis(self, nomes):
        papeis = ["Sabotador"] + ["Anao"] * (len(nomes) - 1)
        random.shuffle(papeis)
        return [Jogador(nome, papel) for nome, papel in zip(nomes, papeis)]

    def _distribuir_mao_inicial(self):
        for jogador in self.jogadores:
            for _ in range(5): 
                if self.deck:
                    jogador.comprar_carta(self.deck.pop())

    def verificar_jogada_valida(self, carta: Carta, x: int, y: int) -> bool:
        if (x, y) in self.tabuleiro:
            return False 

        vizinhos = [
            ((x, y+1), 0, 2), # Cima
            ((x+1, y), 1, 3), # Direita
            ((x, y-1), 2, 0), # Baixo
            ((x-1, y), 3, 1)  # Esquerda
        ]
        
        tem_vizinho = False
        
        for coord_viz, meu_lado, lado_vizinho in vizinhos:
            if coord_viz in self.tabuleiro:
                tem_vizinho = True
                carta_vizinha = self.tabuleiro[coord_viz]
                
                minha_conexao = carta.conexoes[meu_lado]
                vizinho_conexao = carta_vizinha.conexoes[lado_vizinho]
                
                if minha_conexao != vizinho_conexao:
                    return False

        return tem_vizinho

    def _caminho_ate_origem(self, x: int, y: int) -> bool:
        fila = deque([(x, y)])
        visitados = set()
        visitados.add((x, y))

        while fila:
            cx, cy = fila.popleft()
            if (cx, cy) == (0, 0):
                return True
            
            carta_atual = self.tabuleiro[(cx, cy)]
            
            moves = [
                ((cx, cy+1), 0, 2), ((cx+1, cy), 1, 3), 
                ((cx, cy-1), 2, 0), ((cx-1, cy), 3, 1)
            ]
            
            for coord_viz, lado_saida, lado_entrada in moves:
                if coord_viz in self.tabuleiro and coord_viz not in visitados:
                    carta_viz = self.tabuleiro[coord_viz]
                    if carta_atual.conexoes[lado_saida] == 1 and carta_viz.conexoes[lado_entrada] == 1:
                        visitados.add(coord_viz)
                        fila.append(coord_viz)
        return False

    def jogar_turno(self, indice_jogador: int, index_carta_mao: int, x: int, y: int):
        if self.vencedor:
            return {"sucesso": False, "msg": f"Jogo acabou! Vencedor: {self.vencedor}"}

        jogador = self.jogadores[indice_jogador]
        carta = jogador.jogar_carta(index_carta_mao)
        
        if not carta:
            return {"sucesso": False, "msg": "Carta inválida"}

        if self.verificar_jogada_valida(carta, x, y):
            self.tabuleiro[(x, y)] = carta
            msg = f"{jogador.nome} colocou {carta.nome} em {x},{y}"
            
            if (x, y) in self.objetivos:
                if self._caminho_ate_origem(x, y):
                    if self.objetivos[(x, y)] == "ouro":
                        self.vencedor = "Anoes"
                        msg += " e ENCONTROU O OURO!"
                    else:
                        msg += " mas era apenas carvão..."
            
            if self.deck:
                jogador.comprar_carta(self.deck.pop())
            
            self.rodada += 1
            return {"sucesso": True, "msg": msg}
        else:
            jogador.mao.append(carta)
            return {"sucesso": False, "msg": "Jogada inválida! Conexões não batem."}

    def estado_atual(self):
        return {
            "rodada": self.rodada,
            "cartas_no_deck": len(self.deck),
            "vencedor": self.vencedor
        }