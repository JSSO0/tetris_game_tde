## 🧩 Estrutura do Código

### 🔷 Classe `Peca`

* **Responsabilidade** : Representa uma peça do Tetris.
* **Métodos-chave** :
* `rotacionar()`: Gira a peça 90° no sentido horário.
* `mover(dx, dy)`: Move a peça na grade.
* `colide()`: Verifica colisões com bordas ou outras peças.
* `fixar()`: Fixa a peça no tabuleiro.

### 🕹️ Classe `Jogo`

* **Responsabilidade** : Gerencia a lógica principal do jogo.
* **Funcionalidades** :
* `iniciar_jogo()`: Reinicia o estado do jogo.
* `verificar_linhas_completas()`: Remove linhas completas e atualiza pontuação.
* `desenhar_grade()`, `desenhar_peca()`, `desenhar_tabuleiro()`: Renderização gráfica.
* `queda_instantanea()`: Faz a peça cair rapidamente.
* `executar()`: Loop principal do jogo.

### 🖌️ Funções de Renderização

* `tela_inicial(tela)`: Exibe a tela de boas-vindas com animação.
* `desenhar_game_over()`: Mostra mensagens meme e imagem em game over.
* `desenhar_pausado()`: Exibe overlay de pausa.

---

## 🎨 Recursos Visuais/Sonoros

* **Efeitos Sonoros** : Sons de queda, linha completa, pausa e game over.
* **Memes Interativos** :
* Mensagens aleatórias ao completar linhas (ex: "TETRIS GOD!").
* Imagem de meme em game over com opacidade ajustada.
* **Tremor de Tela** : Ativado ao completar 3+ linhas simultâneas.

---

## 🚀 Funcionalidades Interessantes

* **Sistema de Níveis** : Velocidade aumenta conforme linhas são eliminadas.
* **Controles** :
* `← →`: Movimento lateral.
* `↑`: Rotação.
* `↓`: Queda rápida.
* `Espaço`: Queda instantânea.
* `P`: Pausa.
* `R`: Reiniciar.
* **Transições Suaves** : Overlays semi-transparentes para pausa/game over.

---

## 📊 Lógica de Pontuação

* **Pontos por linhas** :
* 1 linha: 100 × nível
* 2 linhas: 300 × nível
* 3 linhas: 700 × nível
* 4 linhas (Tetris): 1500 × nível
