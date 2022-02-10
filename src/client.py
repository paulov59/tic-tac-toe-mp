from tabnanny import check
import pygame
from network import Network, wait_player
from pygame.locals import MOUSEBUTTONDOWN, Rect, QUIT
from sys import exit


global matriz
matriz = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]


def pos_matriz(pos):
    if pos == [100, 100]:
        x = 0; y = 0
    elif pos == [300, 100]:
        x = 0; y = 1
    elif pos == [500, 100]:
        x = 0; y = 2
    elif pos == [100, 300]:
        x = 1; y = 0
    elif pos == [300, 300]:
        x = 1; y = 1
    elif pos == [500, 300]:
        x = 1; y = 2
    elif pos == [100, 500]:
        x = 2; y = 0
    elif pos == [300, 500]:
        x = 2; y = 1
    elif pos == [500, 500]:
        x = 2; y = 2
    
    return x, y


def jogada_matriz(pos, VEZ):
    player = 'X'
    if VEZ == 2:
        player = 'O'
    x, y = pos_matriz(pos)
    matriz[x][y] = player


def verificar_vencedor():
    for i in range(0,3):
        if matriz[i][0] == matriz[i][1] == matriz[i][2]:
            return matriz[i][0]

    for i in range(0,3):
        if matriz[0][i] == matriz[1][i] == matriz[2][i]:
            return matriz[0][i]

    if matriz[0][0] == matriz[1][1] == matriz[2][2]:
        return matriz[0][0]

    if matriz[0][2] == matriz[1][1] == matriz[2][0]:
        return matriz[0][2]

    return ' '


def velha():
    for i in range(0,3):
        for j in range(0,3):
            if matriz[i][j] == ' ':
                return False
    return True


def desenhar_tabuleiro():
    pygame.draw.line(tela, (255, 255, 255), (200, 40), (200, 560), 10) 
    pygame.draw.line(tela, (255, 255, 255), (400, 40), (400, 560), 10)
    pygame.draw.line(tela, (255, 255, 255), (40, 200), (560, 200), 10)
    pygame.draw.line(tela, (255, 255, 255), (40, 400), (560, 400), 10)  


def desenhar_jogada(pos, quemjogou): 
    x, y = pos
    if quemjogou == 2:
        img = pygame.image.load('O.png').convert_alpha()
        imgR = pygame.transform.scale(img, (150, 150)) 
        tela.blit(imgR, (x - 75, y - 75))
    else:
        img = pygame.image.load('X.png').convert_alpha()
        imgR = pygame.transform.scale(img, (150, 150))
        tela.blit(imgR, (x - 75, y - 75))


def jogada():
    for p in rec:
        if e.type == MOUSEBUTTONDOWN and p.collidepoint(mouse_pos):
            if p == rect1:
                confirmar_jogada([100, 100])
            if p == rect2:
                confirmar_jogada([300, 100])
            if p == rect3:
                confirmar_jogada([500, 100])
            if p == rect4:
                confirmar_jogada([100, 300])
            if p == rect5:
                confirmar_jogada([300, 300])
            if p == rect6:
                confirmar_jogada([500, 300])
            if p == rect7:
                confirmar_jogada([100, 500])
            if p == rect8:
                confirmar_jogada([300, 500])
            if p == rect9:
                confirmar_jogada([500, 500])


def confirmar_jogada(pos):
    global ESCOLHA, VEZ, espaco, rede, jogador
    x, y = pos_matriz(pos)
    if matriz[x][y] == 'X':
        print('X')
    elif matriz[x][y] == 'O':
        print('O')
    else:
        matriz[x][y] = ESCOLHA
        desenhar_jogada(pos, jogador)
        jogada_matriz(pos, VEZ)
        print(matriz)
        if VEZ == 1:
            VEZ = 2
        else:
            VEZ = 1
        espaco +=1
    rede.send(f"jogada {str(jogador)} {str(pos[0])} {str(pos[1])}")


def resultado(v):
    opensans = pygame.font.SysFont('opensanscondensed', 45)
    mensagem = 'JOGADOR {} VENCEU'.format(v) 

    if v == 'EMPATE':
        mens_vitoria = opensans.render('DEU VELHA', True, (0, 0, 0), (255, 255, 255))
        tela.blit(mens_vitoria, (115, 265))
    else:
        mens_vitoria = opensans.render(mensagem, True, (0, 0, 0), (255, 255, 255)) 
        tela.blit(mens_vitoria, (100, 265))


def reset():
    global ESCOLHA, ESTADO, VEZ, marca_tabu, espaco
    ESTADO = 'JOGANDO'
    VEZ = 1
    ESCOLHA = 'X'
    espaco = 0
    marca_tabu = [
        0, 1, 2,
        3, 4, 5,
        6, 7, 8
    ]
    tela.fill(0)


pygame.init() 

rede = Network()

tela = pygame.display.set_mode((600, 600), 0, 32)
pygame.display.set_caption('Jogo da velha') 
tela.fill((0, 0, 0)) 
jogador = wait_player(rede, tela)
print(f'jogador: {jogador}')

ESTADO = 'JOGANDO'
VEZ = 1
ESCOLHA = 'X'
espaco = 0
marca_tabu = [
    0, 1, 2,
    3, 4, 5,
    6, 7, 8
]

rect1 = Rect((0, 0), (200, 200))
rect2 = Rect((200, 0), (200, 200))
rect3 = Rect((400, 0), (200, 200))
rect4 = Rect((0, 200), (200, 200))
rect5 = Rect((200, 200), (200, 200))
rect6 = Rect((400, 200), (200, 200))
rect7 = Rect((0, 400), (200, 200))
rect8 = Rect((200, 400), (200, 200))
rect9 = Rect((400, 400), (200, 200))

rec = [
    rect1,rect2,rect3,rect4,
    rect5,rect6,rect7,rect8,rect9,
]

tela.fill((0, 0, 0)) 
while True:
    mouse_pos = pygame.mouse.get_pos()
    if ESTADO == 'JOGANDO':
        desenhar_tabuleiro()
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()
            if e.type == MOUSEBUTTONDOWN:
                if VEZ == jogador:
                    if jogador == 1:
                        ESCOLHA = 'X'
                    else:
                        ESCOLHA = 'O'
                    jogada()

        check = verificar_vencedor()
        if check == 'X':
            rede.send("vitoria 1")
            print('X VENCEU')
            resultado('X')
            ESTADO = 'RESET' 
        elif check == 'O':
            rede.send("vitoria 2")
            print('O VENCEU')
            resultado('O')
            ESTADO = 'RESET'
        elif velha():
            print('EMPATE')
            resultado('EMPATE')
            ESTADO = 'RESET'
    else: 
        for u in pygame.event.get():
            if u.type == QUIT:
                pygame.quit()
                exit()
            if u.type == MOUSEBUTTONDOWN:
                reset()
                desenhar_tabuleiro()

    pygame.display.flip()
    response = rede.send(f"updatevez {str(VEZ)}")
    response = response.split(' ')

    if response[0] == "venceu":
        if response[1] == '1':
            resultado('X')
        else:
            resultado('O')
    if response[0] == 'u':
        VEZ = int(response[1])
        quemjogou = int(response[2])
        x = int(response[3])
        y = int(response[4])
        desenhar_jogada([x, y], quemjogou)
