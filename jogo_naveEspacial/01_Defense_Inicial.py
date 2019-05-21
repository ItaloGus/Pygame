import pygame, sys
from pygame.locals import *
altura = 600
largura = 1000

class Bala(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagemBala = pygame.image.load('imagens/bala.jpg')

        self.rect = self.imagemBala.get_rect()
        self.velocidadeBala = 5
        self.rect.top = posy
        self.rect.left = posx

    def trajetoria(self):
        self.rect.top = self.rect.top - self.velocidadeBala

    def colocar(self, superficie):
        superficie.blit(self.imagemBala, self.rect)
        self.trajetoria()

class nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemNave = pygame.image.load('imagens/Nave.png')

        self.rect = self.ImagemNave.get_rect()
        self.rect.centerx = largura/2
        self.rect.centery = altura - 50

        self.listaDisparo = []
        self.vida = True
        self.velocidade = 20
    
    def __movimento(self):
        if self.vida == True:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > largura + 10:
                self.rect.right = largura + 10
            elif self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom > altura:
                self.rect.bottom = altura

    def movimento_direita(self):
        self.rect.centerx += self.velocidade
        self.__movimento()

    def movimento_esquerda(self):
        self.rect.centerx -= self.velocidade
        self.__movimento()

    def movimento_cima(self):
        self.rect.centery -= self.velocidade
        self.__movimento()

    def movimento_baixo(self):
         self.rect.centery += self.velocidade
         self.__movimento()

    def disparar(self, x , y):
        tiroBala = Bala(x,y)
        self.listaDisparo.append(tiroBala)

    def colocar(self,superficie):
        superficie.blit(self.ImagemNave,self.rect)

def defendendoTerra():
    pygame.init()
    tela = pygame.display.set_mode([largura,altura])
    #relogio = pygame.time.Clock()
    #sair = False
    pygame.display.set_caption('Defense of the Earth')

    player = nave()
    ImagemFundo = pygame.image.load('imagens/espaco.jpg')
    jogando = True

    BalaTrajetoria = Bala(largura / 2, altura - 50)
    relogio = pygame.time.Clock()    
    while True:
        relogio.tick(50)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
                #sair = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == K_LEFT:
                    player.movimento_esquerda()
                if evento.key == K_RIGHT:
                    player.movimento_direita()
                if evento.key == K_UP:
                    player.movimento_cima()
                if evento.key == K_DOWN:
                    player.movimento_baixo()
                if evento.key == K_SPACE:
                    x,y = player.rect.center
                    player.disparar(x,y)
                
        tela.blit(ImagemFundo, (0,0))
        BalaTrajetoria.colocar(tela)
        player.colocar(tela)
        if len(player.listaDisparo) > 0:
            for x in player.listaDisparo:
                x.colocar(tela)
                if x.rect.top < -10:
                    player.listaDisparo.remove(x)
        #relogio.tick(30)
        #tela.fill([255,255,255])
        pygame.display.update()

defendendoTerra()
