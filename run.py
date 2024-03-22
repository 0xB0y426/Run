import pygame
import random
import time

# Create by unoxys

pygame.init()

PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)

largura_tela = 1200
altura_tela = 800

tamanho_quadrado = 40

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Run")

fonte_game_over = pygame.font.SysFont(None, 100)
fonte_vitoria = pygame.font.SysFont(None, 60)

pygame.mixer.init()

clock = pygame.time.Clock()

class Porta:
    def __init__(self):
        self.largura = tamanho_quadrado // 2
        self.altura = tamanho_quadrado
        self.x = random.randint(0, largura_tela - self.largura * 2)
        self.y = random.randint(0, altura_tela - self.altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, BRANCO, [self.x, self.y, self.largura, self.altura])
        pygame.draw.rect(tela, BRANCO, [self.x + self.largura, self.y, self.largura, self.altura])

def desenhar_jogador(x, y):
    pygame.draw.rect(tela, VERDE, [x, y, tamanho_quadrado, tamanho_quadrado])

def desenhar_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, VERMELHO, obstaculo)

def movimentar_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        direcao_x = random.choice([-20, 20])  
        direcao_y = random.choice([-25, 25])  
        obstaculo.x += direcao_x
        obstaculo.y += direcao_y
        obstaculo.x = max(0, min(obstaculo.x, largura_tela - tamanho_quadrado))
        obstaculo.y = max(0, min(obstaculo.y, altura_tela - tamanho_quadrado))

def mostrar_mensagem_game_over():
    mensagem_surface = fonte_game_over.render("Game Over", True, VERMELHO)
    tela.blit(mensagem_surface, (largura_tela // 2 - mensagem_surface.get_width() // 2, altura_tela // 2 - mensagem_surface.get_height() // 2))
    pygame.display.update()

def mostrar_mensagem_vitoria():
    mensagem_surface = fonte_vitoria.render("Você Venceu!", True, VERDE)
    tela.blit(mensagem_surface, (largura_tela // 2 - mensagem_surface.get_width() // 2, altura_tela // 2 - mensagem_surface.get_height() // 2))
    pygame.display.update()

fonte_saida = pygame.font.SysFont(None, 60)

def mostrar_mensagem_saida():
    for _ in range(5):
        tela.fill(VERMELHO)
        mensagem_surface = fonte_saida.render("Você saiu!", True, PRETO)
        tela.blit(mensagem_surface, (largura_tela // 2 - mensagem_surface.get_width() // 2, altura_tela // 2 - mensagem_surface.get_height() // 2))
        pygame.display.update()
        time.sleep(0.5)
        tela.fill(AMARELO)
        mensagem_surface = fonte_saida.render("Você saiu!", True, PRETO)
        tela.blit(mensagem_surface, (largura_tela // 2 - mensagem_surface.get_width() // 2, altura_tela // 2 - mensagem_surface.get_height() // 2))
        pygame.display.update()
        time.sleep(0.5)

def jogo():
    x = 50
    y = 50

    jogador_se_moveu = False

    velocidade = 9

    obstaculos = []

    for _ in range(10):
        obstaculo = pygame.Rect(random.randint(0, largura_tela - tamanho_quadrado), random.randint(0, altura_tela - tamanho_quadrado), tamanho_quadrado, tamanho_quadrado)
        obstaculos.append(obstaculo)

    porta = Porta()

    jogo_ativo = True
    venceu = False
    while jogo_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    mostrar_mensagem_saida()
                    time.sleep(5)
                    pygame.quit()

        teclas = pygame.key.get_pressed()
        if not jogador_se_moveu:
            if any(teclas):
                jogador_se_moveu = True

        if jogador_se_moveu:
            if teclas[pygame.K_LEFT] and x > 0:
                x -= velocidade
            if teclas[pygame.K_RIGHT] and x < largura_tela - tamanho_quadrado:
                x += velocidade
            if teclas[pygame.K_UP] and y > 0:
                y -= velocidade
            if teclas[pygame.K_DOWN] and y < altura_tela - tamanho_quadrado:
                y += velocidade

        movimentar_obstaculos(obstaculos)

        jogador = pygame.Rect(x, y, tamanho_quadrado, tamanho_quadrado)

        if jogador.colliderect(pygame.Rect(porta.x, porta.y, porta.largura * 2, porta.altura)):
            venceu = True
            jogo_ativo = False

        for obstaculo in obstaculos:
            if jogador.colliderect(obstaculo):
                jogo_ativo = False

        tela.fill(PRETO)

        desenhar_obstaculos(obstaculos)

        desenhar_jogador(x, y)

        porta.desenhar(tela)

        pygame.display.update()

        clock.tick(30)

    pygame.mixer.music.stop()

    if venceu:
        mostrar_mensagem_vitoria()
        time.sleep(5)
        jogo()
    else:
        mostrar_mensagem_game_over()
        time.sleep(5)
        pygame.quit()

jogo()
