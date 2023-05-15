import pygame as pg
#import pygame.math.lerp as lerp
def lerp(a, b, percentage):
    if 0.0 > percentage > 1.0:
        raise ValueError("valor deve estar entre 0 e 1")
    return a + (b-a) * percentage
    
class Botao():
	def __init__(self, x, y, cenaManager, funcao=None, funcionarPressionando=False):
		self.cenaManager = cenaManager
		self.funcionarPressionando = funcionarPressionando
		self.funcao = funcao
		self.funcaoSolto = None
		self.imgNormal = None
		self.imgPressionando = None
		self.img = None
		self.travar = False
		if self.imgNormal:
			self.Rect = pg.Rect((x, y), self.img.get_size())
		else:
			self.Rect = pg.Rect((x, y), (16, 16))
		self.pressionado = False
	
	def travarBotao(self, evento=False):
		self.travar = True
		self.pressionado = False
		if evento: self.cenaManager.estados[self.cenaManager.estado].eventoManager.terminouAcao = True
		
	def destravarBotao(self, evento=False):
		self.travar = False
		if evento: self.cenaManager.estados[self.cenaManager.estado].eventoManager.terminouAcao = True
		
	def setFuncao(self, funcao, funcionarPressionando):
		self.funcao = funcao
		self.funcionarPressionando = funcionarPressionando
	def setFuncaoSolto(self, funcao):
		self.funcaoSolto = funcao
		
	def pressionandoMouse(self, mousePos):
		if self.travar: return
		if self.Rect.collidepoint(mousePos):
			if not self.pressionado:
				if self.funcao:
					self.funcao()
			self.pressionado = True
		else:
			self.pressionado = False
	
	def tirandoMouse(self, mousePos):
		if self.travar: return
		if self.Rect.collidepoint(mousePos):
			self.pressionado = False
			if self.funcaoSolto:
				self.funcaoSolto()
	
	def update(self):
		if not self.pressionado or not self.funcionarPressionando:	return
		self.funcao()
		
	def show(self, display, spriteManager):
		if not self.pressionado and self.imgNormal:
			img = spriteManager.load("spritesheets/ui", self.imgNormal)
			img.set_alpha(64+32)
			display.blit(img, self.Rect)
		elif self.pressionado and self.imgPressionando:
			img = spriteManager.load("spritesheets/ui", self.imgPressionando)
			img.set_alpha(128+32)
			display.blit(img, self.Rect)
		else:
			pg.draw.rect(display, (120, 140, 120), self.Rect)

class TopDownMenu:
	def __init__(self, cenaManager, x, y, escolhas, funcoes):
		self.cenaManager = cenaManager
		self.x = x
		self.y = y
		self.escolhas = escolhas
		self.funcoes = funcoes
		self.opcaoAtual = 0
		self.ativo = False
		self.fonte = pg.font.Font("recursos/sprites/fonte.ttf", 8)
		self.menuImg = pg.image.load("recursos/sprites/topdown_menu.png").convert()
		self.indexImg = pg.image.load("recursos/sprites/batalha/index.png").convert()
		self.indexImg.set_colorkey((100, 100, 100))
		self.menuImg.set_colorkey((100, 100, 100))
		#self.cores = [pg.Color]
	
	def toggle(self):
		self.ativo = not self.ativo
		self.cenaManager.botoes["cima"].funcionarPressionando = not self.cenaManager.botoes["cima"].funcionarPressionando
		self.cenaManager.botoes["baixo"].funcionarPressionando = not self.cenaManager.botoes["baixo"].funcionarPressionando
		
	def mover(self, valor):
		self.opcaoAtual += valor
		if self.opcaoAtual<0:
			self.opcaoAtual = len(self.escolhas)-1
		elif self.opcaoAtual==len(self.escolhas):
			self.opcaoAtual = 0
	
	def ativarEscolha(self):
		if not self.funcoes[self.opcaoAtual]:
			self.cenaManager.estados[self.cenaManager.estado].dialogoManager.comecarDialogo(["botao ainda nao implementado."])
		else:
			self.funcoes[self.opcaoAtual]()
		
	def show(self, display):
		display.blit(self.menuImg, (self.x, self.y))
		for i, escolha in enumerate(self.escolhas):
			cor = (0, 0, 0) if i==self.opcaoAtual else (116, 151, 166)
			display.blit(self.fonte.render(escolha, 0, cor, (255, 255, 255)), (self.x+16, self.y+16*i+8))
		display.blit(self.indexImg, (self.x+8, self.y+16*self.opcaoAtual+8))