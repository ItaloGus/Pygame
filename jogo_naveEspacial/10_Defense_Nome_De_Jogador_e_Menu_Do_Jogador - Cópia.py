import pygame, sys, random, os, time
from pygame.locals import *
altura = 600
largura = 1000

WHITE = (255,255,255)
BLACK = (0,0,0)
VERMELHO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)

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

        self.posImagem = 0
        self.listaImagens = [self.imagemInimigo1, self.imagemInimigo2]
        self.imagemAlien = self.listaImagens[self.posImagem]
        self.rect = self.imagemAlien.get_rect()

        self.listaInimigos = []
        self.listaRects = []
        self.listaInimigos2 = []
        self.listaRects2 = []
        self.lisPos = 0
        self.PercorrerLista = 0
        self.velocidade = 1
        self.rect.top = 50
        self.rect.left = aleatorio() - 70
        self.configTempo = 0

    def acertouVarios(self, inimigo, nave):
        for x in nave.listaDisparo:
            posicaoPersonagem = 0 
            for y in inimigo.listaRects:
                if (x.rect.top <= y.top) and (x.rect.left+4 >= y.left-10 and x.rect.right-6 <= y.right):
                    inimigo.listaInimigos[posicaoPersonagem] = inimigo.explosao
                posicaoPersonagem += 1

    def trajetoriaVarios(self):
        self.listaRects[self.PercorrerLista].top += self.velocidade

    def comportamentoVarios(self, tempo):
        
        if self.configTempo == tempo:
            self.variosInimigos()
            self.lisPos += 1
            self.configTempo += 2
        
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
        self.nomeJogador = ''
        self.ImagemNave = pygame.image.load('imagens/Nave3.png')

        self.rect = self.ImagemNave.get_rect()
        self.rect.centerx = largura/2
        self.rect.centery = altura - 50

        self.NumeroPlacar = 0
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

def menu(tela, player):
    #Texto
    fontJogador = pygame.font.SysFont(None, 20)
    fontTitulo = pygame.font.SysFont('Arial', 40, False, True)
    textJogador = fontJogador.render("Digite o nome do Jogador:", True, WHITE)
    digiteNome = fontTitulo.render('DIGITE O NOME DO JOGADOR!', True, VERDE)
    menuJogador = pygame.image.load('imagens/menu3.png')
    ImagemNave = pygame.image.load('imagens/Nave4.png')
    menu_start = pygame.image.load('imagens/menu_start4.png')
    menu_sair = pygame.image.load('imagens/menu_sair2.png')
    
    relogio = pygame.time.Clock()
    sair = False
    animacaoNave = 0
    while sair != True:
        nomeJogador = fontJogador.render(player.nomeJogador , True, WHITE)
        relogio.tick(30)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
                
             #Clique do mouse   
            if evento.type == MOUSEBUTTONDOWN:
                #Entrar no jogo
                for x in range(310,380):
                    for y in range(410,480):
                        if pygame.mouse.get_pos() == (x, y):
                            if player.nomeJogador != '':
                                sair = True
                            else:
                                tela.fill(0)
                                tela.blit(menuJogador, (0,0))
                                tela.blit(digiteNome, [300,altura/2])
                                tela.blit(ImagemNave, [animacaoNave,50])
                                tela.blit(menu_start, [300,400])
                                tela.blit(menu_sair, (880,480))

                                pygame.display.update()
                                time.sleep(2)
                            
                #Sair do jogo
                for x in range(880,980):
                    for y in range(480,580):
                        if pygame.mouse.get_pos() == (x,y):
                            pygame.quit()
                            sys.exit()
            #Teclado        
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_a:
                    player.nomeJogador += 'a'
                if evento.key == K_b:
                    player.nomeJogador += 'b'
                if evento.key == K_c:
                    player.nomeJogador += 'c'
                if evento.key == K_d:
                    player.nomeJogador += 'd'
                if evento.key == K_e:
                    player.nomeJogador += 'e'
                if evento.key == K_f:
                    player.nomeJogador += 'f'
                if evento.key == K_g:
                    player.nomeJogador += 'g'
                if evento.key == K_h:
                    player.nomeJogador += 'h'
                if evento.key == K_i:
                    player.nomeJogador += 'i'
                if evento.key == K_j:
                    player.nomeJogador += 'j'
                if evento.key == K_k:
                    player.nomeJogador += 'k'
                if evento.key == K_l:
                    player.nomeJogador += 'l'
                if evento.key == K_m:
                    player.nomeJogador += 'm'
                if evento.key == K_n:
                    player.nomeJogador += 'n'
                if evento.key == K_o:
                    player.nomeJogador += 'o'
                if evento.key == K_p:
                    player.nomeJogador += 'p'
                if evento.key == K_q:
                    player.nomeJogador += 'q'
                if evento.key == K_r:
                    player.nomeJogador += 'r'
                if evento.key == K_s:
                    player.nomeJogador += 's'
                if evento.key == K_t:
                    player.nomeJogador += 't'
                if evento.key == K_u:
                    player.nomeJogador += 'u'
                if evento.key == K_v:
                    player.nomeJogador += 'v'
                if evento.key == K_w:
                    player.nomeJogador += 'w'
                if evento.key == K_x:
                    player.nomeJogador += 'x'
                if evento.key == K_y:
                    player.nomeJogador += 'y'
                if evento.key == K_z:
                    player.nomeJogador += 'z'
                if evento.key == K_SPACE:
                    player.nomeJogador += ' '
                if evento.key == K_BACKSPACE:
                    player.nomeJogador = ''
                if evento.key == K_RETURN:
                    if player.nomeJogador != '':
                        sair = True
                    else:
                        tela.fill(0)
                        tela.blit(menuJogador, (0,0))
                        tela.blit(digiteNome, [300,altura/2])
                        tela.blit(ImagemNave, [animacaoNave,50])
                        tela.blit(menu_start, [300,400])
                        tela.blit(menu_sair, (880,480))

                        pygame.display.update()
                        time.sleep(2)
                        
        tela.blit(menuJogador, (0,0))
        tela.blit(nomeJogador,[180,20])
        tela.blit(textJogador,[12,20])
        tela.blit(ImagemNave, [animacaoNave,50])

        tela.blit(menu_start, [300,400])
        tela.blit(menu_sair, (880,480))
        
        animacaoNave += 5
        if animacaoNave == 930:
            animacaoNave = 0
        pygame.display.update()

def defendendoTerra():
    tela = pygame.display.set_mode([largura,altura])
    pygame.display.set_caption('Defense of the Earth')
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    player = nave()
    alien = Inimigo()
    menu(tela, player)
    
    alien.configTempo = int(pygame.time.get_ticks()/1000)

    #Texto
    fontJogador = pygame.font.SysFont(None, 20)
    jogador = fontJogador.render(str(player.nomeJogador) , True, WHITE)
    pontuacao = fontJogador.render('PONTUAÇÂO:', True, WHITE)
    perdeuText = fontJogador.render('PERDEU!', True, WHITE)
    
    perdeuImage = pygame.image.load('imagens/perdeu.png')
    ImagemFundo = pygame.image.load('imagens/espaco.jpg')
    
    jogando = True
    perdeu = False

    relogio = pygame.time.Clock()
    while jogando != False:
        placar = fontJogador.render(str(round(player.NumeroPlacar,2)), True, WHITE)
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

        alien.acertouVarios(alien, player)
        if len(alien.listaInimigos) > 0:
            a = 0
            for x in alien.listaRects:
                if x.top >= altura + 10:
                    alien.listaRects.remove(x)
                    alien.listaInimigos.remove(alien.listaInimigos[a])
                    alien.lisPos -= 1
                    if alien.listaInimigos[a] == alien.explosao:
                        player.NumeroPlacar += 10
                    else:
                        perdeu = True
                a += 1
                
        tela.blit(ImagemFundo, (0,0))
        player.colocar(tela)
        alien.colocarVarios(tela, tempo)            
        tela.blit(jogador, [12, 25])
        tela.blit(pontuacao, [12,10])
        tela.blit(placar, [110,10])
        
        if len(player.listaDisparo) > 0:
            for x in player.listaDisparo:
                x.colocar(tela)
                if x.rect.top < -10:
                    player.listaDisparo.remove(x)
        
        if perdeu == True:
            tela.blit(perdeuImage, [largura/2 - 80, altura/2])
        
        pygame.display.flip()

        if perdeu == True:
            jogando = False
            
defendendoTerra()
