#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jogo Tetris implementado em Python usando Pygame
"""

import pygame
import random
import time
from pygame.locals import *

# Inicialização do Pygame
pygame.init()

# Sons
pygame.mixer.music.load("tetris_background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

som_linha = pygame.mixer.Sound("explosion.mp3")
som_gameover = pygame.mixer.Sound("gameover.mp3")
# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
CINZA_ESCURO = (50, 50, 50)

# Cores das peças
CORES = [
    (0, 0, 0),          # Preto (fundo)
    (0, 240, 240),      # Ciano - I
    (0, 0, 240),        # Azul - J
    (240, 160, 0),      # Laranja - L
    (240, 240, 0),      # Amarelo - O
    (0, 240, 0),        # Verde - S
    (160, 0, 240),      # Roxo - T
    (240, 0, 0)         # Vermelho - Z
]
# Mensagens meme
MEMES_LINHA = [
    "TAKE THAT!",
    "EZ PEASY!",
    "TETRIS GOD!",
    "Não para nunca!",
    "Ué, já acabou?",
    "QUE ISSO, INSANO!",
    "Mamãe, to no Tetris!"
]

MEME_GAMEOVER = [
    "Vai jogar Free Fire!",
    "F por você...",
    "Desinstala, campeão!",
    "GAME OVER: nivel Zé Ruela!"
]

# Carrega sons adicionais
som_queda = pygame.mixer.Sound("bruh.mp3")
som_pause = pygame.mixer.Sound("windows_xp_error.mp3")
som_over = pygame.mixer.Sound("fail_trombone.mp3")

# Carrega imagem meme (certifique-se de ter o arquivo)
try:
    meme_img = pygame.image.load("meme_gameover.png")
except FileNotFoundError:
    meme_img = None  # Caso a imagem não exista
# Configurações do jogo
LARGURA_TELA = 800
ALTURA_TELA = 700
LARGURA_GRADE = 10
ALTURA_GRADE = 20
TAMANHO_BLOCO = 30
MARGEM_LATERAL = (LARGURA_TELA - LARGURA_GRADE * TAMANHO_BLOCO) // 2
MARGEM_SUPERIOR = 50

# Configurações de velocidade
FPS = 60
TEMPO_QUEDA_INICIAL = 0.8  # segundos

# Formas das peças (cada número representa um tipo de peça)
PECAS = [
    # Peça vazia (índice 0)
    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    
    # I (índice 1)
    [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    
    # J (índice 2)
    [[2, 0, 0, 0],
     [2, 2, 2, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    
    # L (índice 3)
    [[0, 0, 3, 0],
     [3, 3, 3, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    
    # O (índice 4)
    [[0, 4, 4, 0],
     [0, 4, 4, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    
    # S (índice 5)
    [[0, 5, 5, 0],
     [5, 5, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    
    # T (índice 6)
    [[0, 6, 0, 0],
     [6, 6, 6, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    
    # Z (índice 7)
    [[7, 7, 0, 0],
     [0, 7, 7, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
]
def tela_inicial(tela):
    fonte = pygame.font.SysFont('Arial', 50)
    pequena = pygame.font.SysFont('Arial', 28)
    clock = pygame.time.Clock()
    bounce = 0
    direcao = 1
    while True:
        tela.fill(PRETO)
        bounce += direcao
        if bounce > 10 or bounce < -10:
            direcao *= -1
        texto = fonte.render("TETRIS", True, BRANCO)
        tela.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2,
                          ALTURA_TELA // 3 + bounce))
        iniciar = pequena.render("Pressione qualquer tecla para iniciar", True, BRANCO)
        tela.blit(iniciar, (LARGURA_TELA // 2 - iniciar.get_width() // 2, ALTURA_TELA // 2))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == KEYDOWN:
                return
        clock.tick(FPS)

class Peca:
    """Classe que representa uma peça do Tetris"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo = random.randint(1, 7)  # Escolhe uma peça aleatória (1-7)
        self.rotacao = 0
        self.forma = PECAS[self.tipo]
    
    def rotacionar(self):
        """Rotaciona a peça em 90 graus no sentido horário"""
        # Cria uma nova matriz para a peça rotacionada
        nova_forma = [[0 for _ in range(4)] for _ in range(4)]
        
        # Aplica a rotação
        for i in range(4):
            for j in range(4):
                nova_forma[i][j] = self.forma[3-j][i]
        
        # Verifica se a rotação é válida (não colide com outras peças ou paredes)
        forma_antiga = self.forma
        self.forma = nova_forma
        
        if self.colide():
            self.forma = forma_antiga
            return False
        return True
    
    def mover(self, dx, dy):
        """Move a peça nas direções x e y"""
        self.x += dx
        self.y += dy
        
        # Verifica se o movimento é válido
        if self.colide():
            self.x -= dx
            self.y -= dy
            return False
        return True
    
    def colide(self):
        """Verifica se a peça colide com outras peças ou com as bordas do jogo"""
        for i in range(4):
            for j in range(4):
                if self.forma[i][j] != 0:
                    # Verifica colisão com as bordas
                    if (self.x + j < 0 or self.x + j >= LARGURA_GRADE or 
                        self.y + i >= ALTURA_GRADE):
                        return True
                    
                    # Verifica colisão com outras peças no tabuleiro
                    if self.y + i >= 0 and tabuleiro[self.y + i][self.x + j] != 0:
                        return True
        return False
    
    def fixar(self):
        """Fixa a peça no tabuleiro"""
        for i in range(4):
            for j in range(4):
                if self.forma[i][j] != 0:
                    # Só fixa se a posição estiver dentro do tabuleiro
                    if 0 <= self.y + i < ALTURA_GRADE and 0 <= self.x + j < LARGURA_GRADE:
                        tabuleiro[self.y + i][self.x + j] = self.forma[i][j]

class Jogo:
    """Classe principal do jogo Tetris"""
    
    def __init__(self):
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption('Tetris em Python')
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont('Arial', 25)
        self.fonte_grande = pygame.font.SysFont('Arial', 40)
        self.pontuacao = 0
        self.nivel = 1
        self.linhas_eliminadas = 0
        self.tempo_queda = TEMPO_QUEDA_INICIAL
        self.ultima_queda = time.time()
        self.game_over = False
        self.pausado = False
        self.proxima_peca = Peca(0, 0)
        self.meme_msg = ""
        self.meme_timer = 0
        self.tremor_offset = 0  # Adicione estas três linhas
        self.iniciar_jogo()
    
    def iniciar_jogo(self):
        """Inicializa um novo jogo"""
        global tabuleiro
        tabuleiro = [[0 for _ in range(LARGURA_GRADE)] for _ in range(ALTURA_GRADE)]
        self.peca_atual = Peca(LARGURA_GRADE // 2 - 2, 0)
        self.proxima_peca = Peca(0, 0)
        self.pontuacao = 0
        self.nivel = 1
        self.linhas_eliminadas = 0
        self.tempo_queda = TEMPO_QUEDA_INICIAL
        self.game_over = False
        self.pausado = False
    
    def verificar_linhas_completas(self):
        """Verifica e remove linhas completas, atualizando a pontuação"""
        linhas_completas = 0
        
        for i in range(ALTURA_GRADE):
            completa = True
            for j in range(LARGURA_GRADE):
                if tabuleiro[i][j] == 0:
                    completa = False
                    break
            
            if completa:
                linhas_completas += 1
                # Move todas as linhas acima para baixo
                for y in range(i, 1, -1):
                    for x in range(LARGURA_GRADE):
                        tabuleiro[y][x] = tabuleiro[y-1][x]
                
                # Limpa a linha do topo
                for x in range(LARGURA_GRADE):
                    tabuleiro[0][x] = 0
        
        # Atualiza pontuação e nível
        if linhas_completas > 0:
            self.pontuacao += [0, 100, 300, 700, 1500][linhas_completas] * self.nivel
            self.linhas_eliminadas += linhas_completas
            self.nivel = self.linhas_eliminadas // 10 + 1
            self.tempo_queda = max(0.1, TEMPO_QUEDA_INICIAL - (self.nivel - 1) * 0.05)
            som_linha.play()
            self.meme_msg = random.choice(MEMES_LINHA)
            self.meme_timer = pygame.time.get_ticks() + 2000  # Exibe por 2 segundos
            if linhas_completas >= 3:
                self.tremor_offset = 5
    
    def desenhar_grade(self):
        """Desenha a grade do jogo"""
        # Desenha o fundo da grade
        pygame.draw.rect(self.tela, CINZA_ESCURO, 
                         (MARGEM_LATERAL, MARGEM_SUPERIOR, 
                          LARGURA_GRADE * TAMANHO_BLOCO, 
                          ALTURA_GRADE * TAMANHO_BLOCO))
        
        # Desenha as linhas da grade
        for i in range(ALTURA_GRADE + 1):
            pygame.draw.line(self.tela, CINZA, 
                            (MARGEM_LATERAL, MARGEM_SUPERIOR + i * TAMANHO_BLOCO),
                            (MARGEM_LATERAL + LARGURA_GRADE * TAMANHO_BLOCO, 
                             MARGEM_SUPERIOR + i * TAMANHO_BLOCO))
        
        for j in range(LARGURA_GRADE + 1):
            pygame.draw.line(self.tela, CINZA,
                            (MARGEM_LATERAL + j * TAMANHO_BLOCO, MARGEM_SUPERIOR),
                            (MARGEM_LATERAL + j * TAMANHO_BLOCO, 
                             MARGEM_SUPERIOR + ALTURA_GRADE * TAMANHO_BLOCO))
    
    def desenhar_peca(self, peca, offset_x=0, offset_y=0):
        """Desenha uma peça na tela"""
        for i in range(4):
            for j in range(4):
                if peca.forma[i][j] != 0:
                    pygame.draw.rect(
                        self.tela, 
                        CORES[peca.forma[i][j]],
                        (MARGEM_LATERAL + (peca.x + j + offset_x) * TAMANHO_BLOCO,
                         MARGEM_SUPERIOR + (peca.y + i + offset_y) * TAMANHO_BLOCO,
                         TAMANHO_BLOCO, TAMANHO_BLOCO)
                    )
                    pygame.draw.rect(
                        self.tela, 
                        BRANCO,
                        (MARGEM_LATERAL + (peca.x + j + offset_x) * TAMANHO_BLOCO,
                         MARGEM_SUPERIOR + (peca.y + i + offset_y) * TAMANHO_BLOCO,
                         TAMANHO_BLOCO, TAMANHO_BLOCO),
                        1  # Espessura da borda
                    )
    
    def desenhar_tabuleiro(self):
        """Desenha o tabuleiro com as peças fixas"""
        for i in range(ALTURA_GRADE):
            for j in range(LARGURA_GRADE):
                if tabuleiro[i][j] != 0:
                    pygame.draw.rect(
                        self.tela, 
                        CORES[tabuleiro[i][j]],
                        (MARGEM_LATERAL + j * TAMANHO_BLOCO,
                         MARGEM_SUPERIOR + i * TAMANHO_BLOCO,
                         TAMANHO_BLOCO, TAMANHO_BLOCO)
                    )
                    pygame.draw.rect(
                        self.tela, 
                        BRANCO,
                        (MARGEM_LATERAL + j * TAMANHO_BLOCO,
                         MARGEM_SUPERIOR + i * TAMANHO_BLOCO,
                         TAMANHO_BLOCO, TAMANHO_BLOCO),
                        1  # Espessura da borda
                    )
    
    def desenhar_proxima_peca(self):
        """Desenha a próxima peça na área lateral"""
        # Área para a próxima peça
        pygame.draw.rect(self.tela, CINZA_ESCURO, 
                         (MARGEM_LATERAL + LARGURA_GRADE * TAMANHO_BLOCO + 20, 
                          MARGEM_SUPERIOR, 150, 150))
        
        texto = self.fonte.render("Próxima peça:", True, BRANCO)
        self.tela.blit(texto, (MARGEM_LATERAL + LARGURA_GRADE * TAMANHO_BLOCO + 25, 
                              MARGEM_SUPERIOR - 30))
        
        # Centraliza a próxima peça na área
        offset_x = LARGURA_GRADE + 2
        offset_y = 2
        
        for i in range(4):
            for j in range(4):
                if self.proxima_peca.forma[i][j] != 0:
                    pygame.draw.rect(
                        self.tela, 
                        CORES[self.proxima_peca.forma[i][j]],
                        (MARGEM_LATERAL + (offset_x + j) * TAMANHO_BLOCO,
                         MARGEM_SUPERIOR + (offset_y + i) * TAMANHO_BLOCO,
                         TAMANHO_BLOCO, TAMANHO_BLOCO)
                    )
                    pygame.draw.rect(
                        self.tela, 
                        BRANCO,
                        (MARGEM_LATERAL + (offset_x + j) * TAMANHO_BLOCO,
                         MARGEM_SUPERIOR + (offset_y + i) * TAMANHO_BLOCO,
                         TAMANHO_BLOCO, TAMANHO_BLOCO),
                        1  # Espessura da borda
                    )
    
    def desenhar_informacoes(self):
        """Desenha informações do jogo como pontuação e nível"""
        # Exibe mensagem meme temporária
        if self.meme_msg and pygame.time.get_ticks() < self.meme_timer:
            meme = self.fonte_grande.render(self.meme_msg, True, (255, 255, 0))
            self.tela.blit(meme, (MARGEM_LATERAL, ALTURA_TELA - 80))
        else:
            self.meme_msg = ""
        # Área de informações
        info_x = MARGEM_LATERAL + LARGURA_GRADE * TAMANHO_BLOCO + 20
        info_y = MARGEM_SUPERIOR + 180
        
        # Pontuação
        texto = self.fonte.render(f"Pontuação: {self.pontuacao}", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y))
        
        # Nível
        texto = self.fonte.render(f"Nível: {self.nivel}", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y + 40))
        
        # Linhas eliminadas
        texto = self.fonte.render(f"Linhas: {self.linhas_eliminadas}", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y + 80))
        
        # Controles
        texto = self.fonte.render("Controles:", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y + 140))
        
        texto = self.fonte.render("← → : Mover", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y + 180))
        
        texto = self.fonte.render("↑ : Rotacionar", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y + 210))
        
        texto = self.fonte.render("↓ : Queda rápida", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y + 240))
        
        texto = self.fonte.render("Espaço : Queda instantânea", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y + 270))
        
        texto = self.fonte.render("P : Pausar", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y + 300))
        
        texto = self.fonte.render("R : Reiniciar", True, BRANCO)
        self.tela.blit(texto, (info_x, info_y + 330))
    
    def desenhar_game_over(self):
        """Desenha a tela de game over"""
        som_over.play()
        # Camada semi-transparente
        s = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.tela.blit(s, (0, 0))

        # Texto principal
        texto = self.fonte_grande.render("GAME OVER", True, BRANCO)
        self.tela.blit(texto, (LARGURA_TELA//2 - texto.get_width()//2, ALTURA_TELA//2 - 50))
        
        texto = self.fonte.render(f"Pontuação final: {self.pontuacao}", True, BRANCO)
        self.tela.blit(texto, (LARGURA_TELA//2 - texto.get_width()//2, ALTURA_TELA//2))
        
        texto = self.fonte.render("Pressione R para reiniciar", True, BRANCO)
        self.tela.blit(texto, (LARGURA_TELA//2 - texto.get_width()//2, ALTURA_TELA//2 + 50))

        # Mensagem meme
        meme_text = random.choice(MEME_GAMEOVER)
        t = self.fonte.render(meme_text, True, (255, 255, 0))
        self.tela.blit(t, (LARGURA_TELA//2 - t.get_width()//2, ALTURA_TELA//2 + 80))

        # Imagem meme (centralizada abaixo do texto)
        if meme_img:
            img_rect = meme_img.get_rect(center=(LARGURA_TELA//2, ALTURA_TELA//2 + 160))
            self.tela.blit(meme_img, img_rect)
    
    def desenhar_pausado(self):
        """Desenha a tela de jogo pausado"""
        # Cria uma superfície semi-transparente
        s = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))  # Preto semi-transparente
        self.tela.blit(s, (0, 0))
        
        # Texto de Pausado
        texto = self.fonte_grande.render("JOGO PAUSADO", True, BRANCO)
        self.tela.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2, 
                              ALTURA_TELA // 2 - 25))
        
        # Instruções para continuar
        texto = self.fonte.render("Pressione P para continuar", True, BRANCO)
        self.tela.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2, 
                              ALTURA_TELA // 2 + 25))
    
    def queda_instantanea(self):
        """Faz a peça cair instantaneamente até o fundo"""
        som_queda.play()
        while self.peca_atual.mover(0, 1):
            pass
        self.peca_atual.fixar()
        self.verificar_linhas_completas()
        self.peca_atual = self.proxima_peca
        self.proxima_peca = Peca(LARGURA_GRADE // 2 - 2, 0)
        
        # Verifica se o jogo acabou
        if self.peca_atual.colide():
            self.game_over = True
        
    def executar(self):
        """Loop principal do jogo"""
        while True:
            # Processa eventos
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    return
                
                if evento.type == KEYDOWN:
                    if evento.key == K_r:
                        self.iniciar_jogo()
                    
                    if evento.key == K_p:
                        self.pausado = not self.pausado
                        som_pause.play()
                    
                    if not self.game_over and not self.pausado:
                        if evento.key == K_LEFT:
                            self.peca_atual.mover(-1, 0)
                        elif evento.key == K_RIGHT:
                            self.peca_atual.mover(1, 0)
                        elif evento.key == K_UP:
                            self.peca_atual.rotacionar()
                        elif evento.key == K_DOWN:
                            self.peca_atual.mover(0, 1)
                        elif evento.key == K_SPACE:
                            self.queda_instantanea()

            # Atualiza o jogo se não estiver pausado ou em game over
            if not self.game_over and not self.pausado:
                agora = time.time()
                if agora - self.ultima_queda > self.tempo_queda:
                    self.ultima_queda = agora
                    if not self.peca_atual.mover(0, 1):
                        self.peca_atual.fixar()
                        self.verificar_linhas_completas()
                        self.peca_atual = self.proxima_peca
                        self.proxima_peca = Peca(LARGURA_GRADE // 2 - 2, 0)
                        if self.peca_atual.colide():
                            self.game_over = True

            # Controle da música de fundo
            if pygame.mixer.get_busy():  # Pausa música durante efeitos
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

            # Efeito de tremor
            self.tela.fill(PRETO)
            if self.tremor_offset > 0:
                dx = random.randint(-self.tremor_offset, self.tremor_offset)
                dy = random.randint(-self.tremor_offset, self.tremor_offset)
                self.tela.scroll(dx, dy)
                self.tremor_offset = max(0, self.tremor_offset - 1)

            # Desenha elementos
            self.desenhar_grade()
            self.desenhar_tabuleiro()
            if not self.game_over:
                self.desenhar_peca(self.peca_atual)
            self.desenhar_proxima_peca()
            self.desenhar_informacoes()

            if self.game_over:
                self.desenhar_game_over()
            elif self.pausado:
                self.desenhar_pausado()

            pygame.display.flip()
            self.relogio.tick(FPS)
# Inicializa o tabuleiro global
tabuleiro = [[0 for _ in range(LARGURA_GRADE)] for _ in range(ALTURA_GRADE)]

# Inicia o jogo
if __name__ == "__main__":
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption('Tetris com Animações')
    tela_inicial(tela)
    jogo = Jogo()
    jogo.executar()