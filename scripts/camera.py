from pygame.math import Vector2
from scripts.config import *

class Camera:
	def __init__(self):
		self.x = 0
		self.xAntigo = 0
		self.y = 0
		self.yAntigo = 0

		self.largura = int(DISPLAY_TAMANHO[0]//16)
		self.altura = int(DISPLAY_TAMANHO[1]//16)
	
	def moverPara(self, x, y, mapa):

		self.xAntigo = self.x
		self.yAntigo = self.y
		self.x -= self.x - (x-DISPLAY_TAMANHO[0]//2)
		self.y -= self.y - (y-DISPLAY_TAMANHO[1]//2)
	
	def mudouPosicao(self):
		x = self.x//16
		xAntigo = self.xAntigo//16
		y = self.y//16
		yAntigo = self.yAntigo//16
		return xAntigo!=x or yAntigo!=y