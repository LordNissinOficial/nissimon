import pygame as pg

class Botao():
	def __init__(self, x, y, cenaManager, funcao=None, funcionarPressionando=False):
		self.cenaManager = cenaManager
		self.funcionarPressionando = funcionarPressionando
		self.funcao = funcao
		self.funcaoSolto = None
		self.imgNormal = None
		self.imgPressionando = None
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
	def __init__(self, x, y, escolhas, funcoes):
		self.x = x
		self.y = y
		self.escolhas = escolhas
		self.funcoes = funcoes
		self.opcaoAtual = 0
		self.ativo = False
		self.fonte = pg.font.Font("recursos/sprites/fonte.ttf", 8)
		self.menuImg = pg.image.load("recursos/sprites/topdown_menu.png").convert()
		self.indexImg = pg.image.load("recursos/sprites/batalha/index.png").convert()
		self.menuImg.set_colorkey((100, 100, 100))
	
	def mover(self, valor):
		self.opcaoAtual += valor
		if self.opcaoAtual<0 or self.opcaoAtual==len(self.escolhas):
			self.opcaoAtual -= valor
	
	def ativarEscolha(self):
		self.funcoes[self.opcaoAtual]()
		
	def show(self, display):
		display.blit(self.menuImg, (self.x, self.y))
		for i, escolha in enumerate(self.escolhas):
			display.blit(self.fonte.render(escolha, 0, (0, 0, 0), (255, 255, 255)), (self.x+16, self.y+16*i+8))
		display.blit(self.indexImg, (self.x+8, self.y+16*self.opcaoAtual+8))