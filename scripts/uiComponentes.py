import pygame as pg

class Botao():
	def __init__(self, x, y, funcao=None, funcionarPressionando=False):
		self.funcionarPressionando = funcionarPressionando
		self.funcao = funcao
		self.funcaoSolto = None
		self.imgNormal = None
		self.imgPressionando = None
		if self.imgNormal:
			self.Rect = pg.Rect((x, y), self.img.get_size())
		else:
			self.Rect = pg.Rect((x, y), (16, 16))
		self.pressionado = False
	
	def setFuncao(self, funcao, funcionarPressionando):
		self.funcao = funcao
		self.funcionarPressionando = funcionarPressionando
	def setFuncaoSolto(self, funcao):
		self.funcaoSolto = funcao
		
	def pressionandoMouse(self, mousePos):
		if self.Rect.collidepoint(mousePos):
			if not self.pressionado:
				if self.funcao:
					self.funcao()
			self.pressionado = True
		else:
			self.pressionado = False
	
	def tirandoMouse(self, mousePos):
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
			img.set_alpha(60)
			display.blit(img, self.Rect)
		elif self.pressionado and self.imgPressionando:
			img = spriteManager.load("spritesheets/ui", self.imgPressionando)
			img.set_alpha(128)
			display.blit(img, self.Rect)
		else:
			pg.draw.rect(display, (120, 140, 120), self.Rect)