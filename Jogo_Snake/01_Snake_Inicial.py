#################################################################################
##Importações
import pygame, random, sys, os
from pygame.locals import *
#################################################################################
##Variáveis
a = 0
NumeroPlacar = 0
velocidade = 10
#################################################################################
##Funções
def on_grid_random():
    x = random.randint(10,580)
    y = random.randint(50,380)
    return (x//10 * 10, y//10 * 10)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])
#################################################################################
##Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
#################################################################################
##Iniciando módulos e Tela Centralizada
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

#################################################################################
##Criando tela
screen = pygame.display.set_mode((600,400))
pygame.display.set_caption('IGAMES')

#################################################################################
##Clock do Jogo
clock = pygame.time.Clock()

#################################################################################
##TEXTO no Programa
fontJogador = pygame.font.SysFont(None, 20)
fontTitulo = pygame.font.SysFont('Arial', 14, False, True)
jogador = fontJogador.render('IGOR', True, WHITE)
pontuacao = fontJogador.render('PONTUAÇÂO:', True, WHITE)
saida = fontTitulo.render("Tecle ENTER para SAIR! !", True, WHITE)

#################################################################################
##MAÇA e COBRA (Design)
snake = [(300, 340), (310, 340), (320,340), (330,340)]
snake_skin = pygame.Surface((10,10))
snake_skin.fill((51,51,51))
apple_pos = on_grid_random()
apple = pygame.Surface((10,10))
apple.fill((RED))
#################################################################################
##Botão de Direção
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

my_direction = LEFT
#################################################################################
##JOGO RODANDO e SEUS MOVIMENTOS
sair = False
while sair != True:
    a += 1
    placar = fontJogador.render(str(NumeroPlacar), True, WHITE)
    clock.tick(velocidade)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
                
        if event.type == KEYDOWN:
            if event.key == K_UP:
                if my_direction == DOWN:
                    continue
                my_direction = UP
            if event.key == K_DOWN:
                if my_direction == UP:
                    continue
                my_direction = DOWN
            if event.key == K_LEFT:
                if my_direction == RIGHT:
                    continue
                my_direction = LEFT
            if event.key == K_RIGHT:
                if my_direction == LEFT:
                    continue
                my_direction = RIGHT
            if event.key == K_RETURN:
                sair = True
                
    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random()
        snake.append((0,0))
        NumeroPlacar += 10
        
    ##Limite de Tela
    if (snake[0][0] == 0 or snake[0][1] == 50 or snake[0][0] == 590 or snake[0][1] == 390):
        break
        
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    ##Direção da Cobra
    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - velocidade)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + velocidade)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + velocidade, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - velocidade, snake[0][1])

    screen.fill((255,255,255))
    
    screen.blit(apple, apple_pos)

    for pos in snake:
        screen.blit(snake_skin,pos)
            
    ##CAIXA DO JOGADOR
    pygame.draw.line(screen, BLACK, [1, 1], [600, 1], 5)
    pygame.draw.line(screen, BLACK, [1, 1], [1, 400], 5)    
    pygame.draw.line(screen, BLACK, [600, 1], [600, 400], 10)    
    pygame.draw.line(screen, BLACK, [1, 400], [600, 400], 10)
    pygame.draw.line(screen, BLACK, [1, 50], [600, 50], 5)
    pygame.draw.polygon(screen, (0,0,255), ((5,5) , (5,45), (594,45), (594,5), (5,5)), 0)
    ##TEXTO DO JOGADOR
    screen.blit(jogador, [12, 25])
    screen.blit(pontuacao, [12,10])
    screen.blit(placar, [110,10])
    if(a <= 10):
        screen.blit(saida, [465,30])
    elif(a >= 11 and a <= 20):
        screen.blit(saida, [465,10])
        if(a == 20):
            a = 0
    pygame.display.flip()

pygame.quit()
