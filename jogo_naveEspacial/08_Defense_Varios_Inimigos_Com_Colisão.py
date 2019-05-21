import pygame, sys, random, os
from pygame.locals import *
altura = 600
largura = 1000

def strings():
    pass

def aleatorio():
    x  = random.randint(40, largura - 70)
    return (int(x/10) * 10)

class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagemInimigo1 = pygame.image.load('imagens/alien1.png')
        self.imagemInimigo2 = pygame.image.load('imagens/alien2.png')
        self.explosao = pygame.image.load('imagens/fogo.png')
        
        self.listaImagens = [self.imagemInimigo1, self.imagemInimigo2]
        self.posImagem = 0
        self.imagemAlien = self.listaImagens[self.posImagem]
        
        self.rect = self.imagemAlien.get_rect()

        self.listaInimigos = []
        self.listaRects = []
        self.lisPos = 0
        self.PercorrerLista = 0
        self.velocidade = 1
        self.rect.top = 50
        self.rect.left = aleatorio() - 70
        self.configTempo = 1

    def comportamento(self, tempo):
        if self.configTempo == tempo:
            self.posImagem += 1
            self.configTempo += 1
            if self.posImagem > len(self.listaImagens) - 1:
                self.posImagem = 0
        
    def trajetoria(self):
        self.rect.top += self.velocidade

    
    def colocar(self, superficie, tempo):
        superficie.blit(self.listaImagens[self.posImagem], self.rect)
        #self.comportamento(tempo)
        self.trajetoria()

    def acertouVarios(self, inimigo, nave):
        a = 0
        for x in nave.listaDisparo:
            if (x.rect.top == inimigo.ListaRects[a].top) and (x.rect.left >= inimigo.ListaRects[a].left and x.rect.left+6 <= inimigo.ListaRects[a].right):          
                BalaTrajetoria.acertou = True
                verificacaoDeAcerto = 1
                a += 1

    def trajetoriaVarios(self):
        self.listaRects[self.PercorrerLista].top += self.velocidade

    def comportamentoVarios(self, tempo):
        if self.configTempo*2 == tempo:
            self.variosInimigos()
            self.lisPos += 1
            self.configTempo += 1
            #if self.lisPos > len(self.listaInimigos) - 1:
            #    self.posImagem = 0
        
    def variosInimigos(self):
        self.listaInimigos.append(self.imagemAlien)
        self.listaRects.append(self.listaInimigos[self.lisPos].get_rect())
        self.listaRects[self.lisPos].top = 50
        self.listaRects[self.lisPos].left = aleatorio()

    def colocarVarios(self, superficie, tempo):
        self.comportamentoVarios(tempo)
        self.PercorrerLista = 0
        for x in self.listaInimigos:
            superficie.blit(x, self.listaRects[self.PercorrerLista])
            self.trajetoriaVarios()
            self.PercorrerLista += 1
        
    def colocarExplosao(self,superficie):
        superficie.blit(self.explosao, self.rect)

class Bala(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagemBala = pygame.image.load('imagens/bala.jpg')

        self.rect = self.imagemBala.get_rect()
        self.acertou = False
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
        self.ImagemNave = pygame.image.load('imagens/Nave3.png')

        self.rect = self.ImagemNave.get_rect()
        self.rect.centerx = largura/2
        self.rect.centery = altura - 50

        self.listaDisparo = []
        self.vida = True
        self.velocidade = 5

        self.movEsq = False
        self.movDir = False
        self.movCima = False
        self.movBaixo = False
    
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
            elif self.rect.top <= 0 and self.rect.left <= 30:
                self.rect.top = 0
            elif self.rect.bottom <= altura and self.rect.left <= 0:
                self.rect.left = 0
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
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    WHITE = (255,255,255)

    #strings()
    
    NumeroPlacar = 0
    fontJogador = pygame.font.SysFont(None, 20)
    jogador = fontJogador.render('Geofran', True, WHITE)
    pontuacao = fontJogador.render('PONTUAÇÂO:', True, WHITE)
    
    tela = pygame.display.set_mode([largura,altura])
    pygame.display.set_caption('Defense of the Earth')
    
    player = nave()
    ImagemFundo = pygame.image.load('imagens/espaco.jpg')
    jogando = True
    verificacaoDeAcerto = 0

    alien = Inimigo()
    
    BalaTrajetoria = Bala(largura / 2, altura - 50)
    relogio = pygame.time.Clock()    
    while jogando != False:
        placar = fontJogador.render(str(NumeroPlacar), True, WHITE)
        relogio.tick(30)
        tempo = int(pygame.time.get_ticks()/1000)
        #print(tempo)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
                #sair = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == K_LEFT:
                    player.movEsq = True
                if evento.key == K_RIGHT:
                    player.movDir = True
                if evento.key == K_UP:
                    player.movCima = True
                if evento.key == K_DOWN:
                    player.movBaixo = True
                if evento.key == K_SPACE:
                    x,y = player.rect.center
                    player.disparar(x,y)

            if evento.type == pygame.KEYUP:
                if evento.key == K_LEFT:
                    player.movEsq = False
                if evento.key == K_RIGHT:
                    player.movDir = False
                if evento.key == K_UP:
                    player.movCima = False
                if evento.key == K_DOWN:
                    player.movBaixo = False

        #correção de limite de tela           
        if player.rect.left <= 0:
            player.movEsq = False
        if player.rect.top <= 0:
            player.movCima = False
        if player.rect.bottom >= altura:
            player.movBaixo = False

        #movimento continuo    
        if player.movEsq == True:
            player.movimento_esquerda()
        if player.movDir == True:
            player.movimento_direita()
        if player.movCima == True:
            player.movimento_cima()
        if player.movBaixo == True:
            player.movimento_baixo()

        #Acertou o inimigo
        for x in player.listaDisparo:     
            posicaoPersonagem = 0
            acertou = 0
            #(x.rect.top == y.top) and 
            for y in alien.listaRects:
                if (x.rect.top <= y.top) and (x.rect.left+4 >= y.left-10 and x.rect.right-6 <= y.right):
                    alien.listaInimigos[posicaoPersonagem] = alien.explosao
                    acertou += 1
                    if acertou >= 1:
                      NumeroPlacar += acertou * 10
                posicaoPersonagem += 1
                acertou = 0
##        if len(alien.listaInimigos) > 0:       
##            a = 0
##            for x in alien.listaInimigos:
##                if alien.listaRects[a].bottom >= altura + 10:
##                    alien.listaInimigos.remove(x)
##                    alien.listaRects.remove(x)
##                a += 1
               
        tela.blit(ImagemFundo, (0,0))
        BalaTrajetoria.colocar(tela)
        player.colocar(tela)
        
        #if BalaTrajetoria.acertou != True:
        alien.colocarVarios(tela, tempo)
        #if verificacaoDeAcerto > 0 and verificacaoDeAcerto <= 10:
            #alien.colocarExplosao(tela)
            #verificacaoDeAcerto += 1
        
        if len(player.listaDisparo) > 0:
            for x in player.listaDisparo:
                x.colocar(tela)
                if x.rect.top < -10:
                    player.listaDisparo.remove(x)
                    
        #relogio.tick(30)
        #tela.fill([255,255,255])
        tela.blit(jogador, [12, 25])
        tela.blit(pontuacao, [12,10])
        tela.blit(placar, [110,10])
        pygame.display.update()

defendendoTerra()
