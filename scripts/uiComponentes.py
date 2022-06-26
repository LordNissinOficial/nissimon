import pygame as pg

class Botao():
	def __init__(self, x, y, funcao=None, funcionarPressionando=False):
		self.funcionarPressionando = funcionarPressionando
		self.funcao = funcao
		self.imgNormal = None#pg.image.load("recursos/sprites/botoes/"+img+".png").convert()
		self.imgPressionando = None
		#self.img.set_colorkey((0, 0, 0))
		if self.imgNormal:
			self.Rect = pg.Rect((x, y), self.img.get_size())
		else:
			self.Rect = pg.Rect((x, y), (16, 16))
		self.pressionado = False

	def pressionandoMouse(self, mousePos):
		if self.Rect.collidepoint(mousePos):
			self.pressionado = True
		else:
			self.pressionado = False
	
	def tirandoMouse(self, mousePos):
		if self.Rect.collidepoint(mousePos):
			self.pressionado = False
			if self.funcao:
				self.funcao()
	
	def update(self):
		if not self.pressionado or not self.funcionarPressionando:	return
		self.funcao()
		
	def show(self, display, spriteManager):
		#pg.draw.rect(dis)
		if not self.pressionado and self.imgNormal:
			display.blit(spriteManager.load("spritesheets/ui", self.imgNormal), self.Rect)
			#display.blit(self.imgNormal, self.Rect)
		elif self.pressionado and self.imgPressionando:
			display.blit(spriteManager.load("spritesheets/ui", self.imgPressionando), self.Rect)
			#display.blit(self.imgPressionando, self.Rect)
		else:
			pg.draw.rect(display, (120, 140, 120), self.Rect)
#		if self.pressionado:
#			pg.draw.rect(display, (224, 123, 44), self.Rect)