import pygame as pg

pg.font.init()

class DialogoManager:
	def __init__(self):
		self.caixaTexto = pg.image.load("recursos/sprites/caixa_de_texto.png").convert()
		self.fonte = pg.font.Font("recursos/sprites/fonte.ttf", 8)
		self.texto = ["Iae nissin meu compade!", "como voce esta se sentindo?"]
		self.visivel = [0, 0]
		self.emDialogo = False
		self.timerTanto = 1
		self.timer = self.timerTanto

	def comecarDialogo(self, dialogo):
		self.emDialogo = True
		self.texto = dialogo
		self.visivel = [0, 0]
		self.timerTanto = 1
		self.timer = self.timerTanto
		
	def update(self):
		if not self.emDialogo: return
		#print(self.timerTanto)
		if self.timer>0:
			self.timer -= 1
			return

		self.timer = self.timerTanto
		
		if self.visivel[1]+1<len(self.texto[self.visivel[0]]):
			self.visivel[1] += 1
		else:
			if self.visivel[0]==0:
				self.visivel[0] += 1
				self.visivel[1] = 0
#			else:
#				self.emDialogo = False
				
	def show(self, display):
		display.blit(self.caixaTexto, (16, 104))
		if self.visivel[0]==1:
			display.blit(self.fonte.render(self.texto[0], 0, (0, 0, 0), (255, 255, 255)), (24, 110))
			display.blit(self.fonte.render(self.texto[1][0:self.visivel[1]+1], 0, (0, 0, 0), (255, 255, 255)), (24, 126))
		else:
			display.blit(self.fonte.render(self.texto[0][0:self.visivel[1]+1], 0, (0, 0, 0), (255, 255, 255)), (24, 110))
		