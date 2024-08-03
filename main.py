''' 
- configurações iniciais(ex:importar as bibliotecas + configs)

- criar um loop infinito(é o jogo rodando)
    OBS: entre uma execução e outra, o pg precisa de uma pequena pausa para funcionar(para não travar o código + para receber as interações do usuario, desenhar as coisas na TELA)

    - desenhar os objetos do jogo na TELA(pontuação, cobrinha, comida)

    - criar a logica de terminar o jogo
        - o que acontece:
            - cobra comeu maça
            - cobra bateu na parede
            - cabra bateu na propria cobra

    - pegar as interações do usuário(fechar a TELA, apertou as teclas para mover a cobra)

- OBS: cobrinha = lista de pixels
'''

import pygame as pg
import random

pg.init()
pg.display.set_caption("Jogo da Cobrinha")

# Declaração de constantes
TELA_INFO = pg.display.Info()
LARGURA, ALTURA = 1000, 800
TELA = pg.display.set_mode((LARGURA, ALTURA))
RELOGIO = pg.time.Clock()
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
LARANJA = (191, 80, 15)
AZUL = (0, 0, 255)
TAMANHO_QUADRADO = 50

# Carregar imagem da comida
imagem_comida = pg.transform.scale(pg.image.load('images/apple.png'), (int(TAMANHO_QUADRADO * 1.15), int(TAMANHO_QUADRADO * 1.15)))

def gerar_comida():
    comida_x = round(random.randrange(TAMANHO_QUADRADO, LARGURA - TAMANHO_QUADRADO * 2) / TAMANHO_QUADRADO) * TAMANHO_QUADRADO
    comida_y = round(random.randrange(TAMANHO_QUADRADO, ALTURA - TAMANHO_QUADRADO * 2) / TAMANHO_QUADRADO) * TAMANHO_QUADRADO
    return comida_x, comida_y

def desenhar_comida(comida_x, comida_y, resposta):
    fonte = pg.font.SysFont("Helvetica", int(TAMANHO_QUADRADO / 1.5))
    texto = fonte.render(f"{resposta}", True, PRETO)
    
    TELA.blit(imagem_comida, (comida_x, comida_y))
    TELA.blit(texto, (comida_x + TAMANHO_QUADRADO / 4, comida_y + TAMANHO_QUADRADO / 4))

def desenhar_cobra(tamanho, pixels):
    listras = True
    for pixel in pixels:
        cor = PRETO if listras else LARANJA
        pg.draw.rect(TELA, cor, [pixel[0], pixel[1], tamanho, tamanho])
        listras = not listras

def render_texto_contorno(texto, x, y, tamanho_fonte):
    fonte = pg.font.SysFont("Helvetica", tamanho_fonte)
    texto_surface = fonte.render(texto, True, VERMELHO)
    contorno_surface = fonte.render(texto, True, PRETO)
    
    # Desenhar o contorno em várias posições ligeiramente deslocadas
    TELA.blit(contorno_surface, (x - 2, y - 2))
    TELA.blit(contorno_surface, (x + 2, y - 2))
    TELA.blit(contorno_surface, (x - 2, y + 2))
    TELA.blit(contorno_surface, (x + 2, y + 2))
    TELA.blit(contorno_surface, (x - 2, y))
    TELA.blit(contorno_surface, (x + 2, y))
    TELA.blit(contorno_surface, (x, y - 2))
    TELA.blit(contorno_surface, (x, y + 2))

    # Desenhar o texto principal no centro do contorno
    TELA.blit(texto_surface, (x, y))

def selecionar_velocidade(tecla):
    if tecla == pg.K_DOWN:
        velocidade_x = 0
        velocidade_y = TAMANHO_QUADRADO
    elif tecla == pg.K_UP:
        velocidade_x = 0
        velocidade_y = -TAMANHO_QUADRADO
    elif tecla == pg.K_RIGHT:
        velocidade_x = TAMANHO_QUADRADO
        velocidade_y = 0
    elif tecla == pg.K_LEFT:
        velocidade_x = -TAMANHO_QUADRADO
        velocidade_y = 0
    return velocidade_x, velocidade_y

def gerar_conta():
    operacao = random.randint(1, 2)
    num1 = random.randint(1, 50)
    num2 = random.randint(1, 50)
    if operacao == 1:
        return f'{num1} + {num2} = ?', num1 + num2
    else:
        return f'{num1} - {num2} = ?', num1 - num2

def gerar_respostas_erradas(resposta):
    respostas_erradas = set()
    while len(respostas_erradas) < 1:
        errada = resposta + random.randint(-10, 10)
        if errada != resposta:
            respostas_erradas.add(errada)
    return list(respostas_erradas)

def rodar_jogo():
    velocidade_jogo = 10
    fim_jogo = False
    x = LARGURA / 2
    y = ALTURA / 2
    velocidade_x = 0
    velocidade_y = 0
    tamanho_cobra = 1
    pixels = []
    comida_correta_x, comida_correta_y = gerar_comida()
    comida_errada_x, comida_errada_y = gerar_comida()
    while comida_errada_x == comida_correta_x and comida_errada_y == comida_correta_y:
        comida_errada_x, comida_errada_y = gerar_comida()
    label, resposta_correta = gerar_conta()
    resposta_errada = gerar_respostas_erradas(resposta_correta)[0]

    while not fim_jogo:
        TELA.blit(pg.transform.scale(pg.image.load('images/background.png'), (LARGURA, ALTURA)), (0, 0))

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                exit()
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    return tamanho_cobra - 1
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)
        
        desenhar_comida(comida_correta_x, comida_correta_y, resposta_correta)
        desenhar_comida(comida_errada_x, comida_errada_y, resposta_errada)

        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
            fim_jogo = True

        x += velocidade_x
        y += velocidade_y
                
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        if tamanho_cobra < 0:
            fim_jogo = True

        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True

        desenhar_cobra(TAMANHO_QUADRADO, pixels)
        render_texto_contorno(f"Pontos: {tamanho_cobra - 1}", 1, 1, TAMANHO_QUADRADO)
        render_texto_contorno(label, 1, TAMANHO_QUADRADO, TAMANHO_QUADRADO)
        pg.display.update()

        if x == comida_correta_x and y == comida_correta_y:
            tamanho_cobra += 1
            velocidade_jogo += 0.15
            label, resposta_correta = gerar_conta()
            resposta_errada = gerar_respostas_erradas(resposta_correta)[0]
            comida_correta_x, comida_correta_y = gerar_comida()
            comida_errada_x, comida_errada_y = gerar_comida()
            while comida_errada_x == comida_correta_x and comida_errada_y == comida_correta_y:
                comida_errada_x, comida_errada_y = gerar_comida()
        elif x == comida_errada_x and y == comida_errada_y:
            del pixels[0]
            tamanho_cobra -= 1
            comida_errada_x, comida_errada_y = gerar_comida()
            while comida_errada_x == comida_correta_x and comida_errada_y == comida_correta_y:
                comida_errada_x, comida_errada_y = gerar_comida()

        RELOGIO.tick(int(velocidade_jogo))

    return tamanho_cobra - 1

def mostrar_menu(pontuacao_maxima):
    menu_ativo = True
    while menu_ativo:
        TELA.blit(pg.transform.scale(pg.image.load('images/background.png'), (LARGURA, ALTURA)), (0, 0))
        render_texto_contorno("Jogo da Cobrinha", LARGURA // 8, ALTURA // 4, TAMANHO_QUADRADO * 2)
        render_texto_contorno("Pressione ENTER para Jogar", LARGURA // 8, ALTURA // 2, TAMANHO_QUADRADO)
        render_texto_contorno(f"Pontuação Máxima: {pontuacao_maxima}", LARGURA // 8, ALTURA // 2 + TAMANHO_QUADRADO * 2, TAMANHO_QUADRADO)
        render_texto_contorno("Pressione ESC para Sair", LARGURA // 8, ALTURA // 2 + TAMANHO_QUADRADO * 4, TAMANHO_QUADRADO)
        pg.display.update()

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                exit()
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_RETURN:
                    menu_ativo = False
                elif evento.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()

def main():
    pontuacao_maxima = 0
    while True:
        mostrar_menu(pontuacao_maxima)
        pontuacao = rodar_jogo()
        if pontuacao > pontuacao_maxima:
            pontuacao_maxima = pontuacao

if __name__ == "__main__":
    main()