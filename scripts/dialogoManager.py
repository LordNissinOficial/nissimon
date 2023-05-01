import pygame as pg

pg.font.init()

class DialogoManager:
	def __init__(self):
		self.caixaTexto = pg.image.load("recursos/sprites/caixa_de_texto.png").convert()
		self.seta = pg.transform.rotate(pg.image.load("recursos/sprites/batalha/index.png").convert(), -90)
		#sslf.caixaTexto.set_colorkey((255, 255, 255))
		self.fonte = pg.font.Font("recursos/sprites/fonte.ttf", 8)
		self.texto = ["Iae nissin meu compade!", "como voce esta se sentindo?"]
		self.visivel = [0, 0]
		self.evento = False
		self.proximoTexto = [False, 0]
		self.ativouTimer = False
		self.acabarTimer = 0
		self.emDialogo = False
		self.mostrarSeta = 0
		self.timerTanto = 1
		self.timer = self.timerTanto

	def comecarDialogo(self, dialogo, evento=False):
		self.evento=evento
		self.ativouTimer = False
		self.acabarTimer = 0
		self.emDialogo = True
		self.texto = dialogo
		self.visivel = [0, 0]
		self.timerTanto = 1
		self.proximoTexto = [False, 0]
		self.timer = self.timerTanto
		
	def update(self):
		if not self.emDialogo: return
		if self.acabarTimer>0:
			self.acabarTimer-=1
			
		self.mostrarSeta = (self.mostrarSeta+1)%20
		#print(self.timerTanto)
		if self.timer>0:
			self.timer -= 1
			return

		self.timer = self.timerTanto
		
		if self.visivel[1]+1<len(self.texto[self.visivel[0]]):
			
			self.visivel[1] += 1
		elif not (self.visivel[0]+1)%2==0:
			if self.visivel[0]+1<len(self.texto):
				self.visivel[0] += 1
				self.visivel[1] = 0
			else:
				if not self.ativouTimer:
					self.ativouTimer = True
					self.acabarTimer = 15
					
		
		
#			else:
#				self.emDialogo = False
				
	def show(self, display):
		#pg.draw.rect(display, (255, 255, 255), (0, 104, 256, 40))
		display.blit(self.caixaTexto, (0, 104))
		if self.mostrarSeta<14 and self.visivel[0]!=len(self.texto)-1 and (self.visivel[0]+1)%2==0 and self.visivel[1]==len(self.texto[self.visivel[0]])-1: 
			
			display.blit(self.seta, (256-28, 144-7))
		
#		for i in range(max(0, self.visivel[0]-1), self.visivel[0]):
#			display.blit(self.fonte.render(self.texto[0], 0, (0, 0, 0), (255, 255, 255)), (24, 110+16*i%2))
		if self.visivel[0]>0:
			display.blit(self.fonte.render(self.texto[self.visivel[0]-1], 0, (0, 0, 0), (255, 255, 255)), (24, 110))
			display.blit(self.fonte.render(self.texto[self.visivel[0]][0:self.visivel[1]+1], 0, (0, 0, 0), (255, 255, 255)), (24, 126))
		else:
			display.blit(self.fonte.render(self.texto[0][0:self.visivel[1]+1], 0, (0, 0, 0), (255, 255, 255)), (24, 110))
		#if self.visivel[0]==1:
#			display.blit(self.fonte.render(self.texto[0], 0, (0, 0, 0), (255, 255, 255)), (24, 110))
#			display.blit(self.fonte.render(self.texto[1][0:self.visivel[1]+1], 0, (0, 0, 0), (255, 255, 255)), (24, 126))
#		else:
#			display.blit(self.fonte.render(self.texto[0][0:self.visivel[1]+1], 0, (0, 0, 0), (255, 255, 255)), (24, 110))
#		