from pygame.image import load
from scripts.entidade import Entidade
from scripts.uiComponentes import Botao
from scripts.config import *


class Jogador(Entidade):#pg.sprite.Sprite):
	def __init__(self, x, y, jogo):
		self.img = load("recursos/sprites/jogador.png").convert()
		self.img.set_colorkey((0, 0, 0))
		Entidade.__init__(self, x, y, self.img.get_width(), self.img.get_height())

	
	def update(self, jogo, deltaTime):				
		self.updateMovimento(jogo, deltaTime)

	def show(self, display, camera):
		x = self.xMovendo-camera.x
		y = self.yMovendo-camera.y
		display.blit(self.img, (x, y))		