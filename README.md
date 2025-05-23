# Jogo Tetris em Python com Pygame

Este é um jogo de Tetris completo implementado em Python utilizando a biblioteca Pygame.

## Características

- Interface gráfica completa
- Sistema de pontuação
- Níveis de dificuldade progressivos
- Visualização da próxima peça
- Controles intuitivos
- Tela de pausa e game over

## Requisitos

- Python 3.x
- Pygame (instalável via `pip install pygame`)

## Como jogar

1. Certifique-se de ter Python e Pygame instalados
2. Execute o arquivo `tetris.py` com Python:
   ```
   python tetris.py
   ```

## Controles

- **Setas Esquerda/Direita**: Mover peça horizontalmente
- **Seta para Cima**: Rotacionar peça
- **Seta para Baixo**: Queda rápida
- **Espaço**: Queda instantânea
- **P**: Pausar/Continuar jogo
- **R**: Reiniciar jogo

## Regras do Jogo

- As peças caem do topo da tela
- O jogador pode mover e rotacionar as peças enquanto elas caem
- Quando uma linha horizontal é completamente preenchida, ela é eliminada e o jogador ganha pontos
- O jogo termina quando as peças empilhadas atingem o topo da tela
- A velocidade de queda das peças aumenta conforme o jogador avança de nível

## Pontuação

- 1 linha eliminada: 100 pontos × nível atual
- 2 linhas eliminadas: 300 pontos × nível atual
- 3 linhas eliminadas: 700 pontos × nível atual
- 4 linhas eliminadas: 1500 pontos × nível atual

## Estrutura do Código

O jogo é organizado em classes e funções:

- `Peca`: Classe que representa uma peça do Tetris, com métodos para rotação e movimentação
- `Jogo`: Classe principal que gerencia o loop do jogo, desenho na tela e lógica de jogo
- Funções auxiliares para verificação de colisões, linhas completas e game over

## Personalização

Você pode personalizar o jogo modificando as constantes no início do arquivo:
- Cores
- Tamanho da grade
- Tamanho dos blocos
- Velocidade inicial
- Dimensões da tela
