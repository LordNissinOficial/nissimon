from pygame.image import load as loadImage
from pygame.font import (init, Font)
from functools import cache

init()

class SpriteManager():
	def __init__(self):
		self.path = "recursos/sprites/"
		self.spriteAtual = None
		self.fonte = Font("recursos/alagard.ttf", 16)
		#self.fonte.set_underline(True)
		self.sprites = {}
		self.fontes = {}
	
	def underline(bool):
		self.fonte.set_underline(bool)
#	def loadFonte(self):
#		return self.fonte
#		if filename not in self.fontes:
#			self.fonte
	#@cache
	def load(self, filename, rect=None):
		if filename not in self.sprites:
			try:
				self.sprites[filename] = loadImage(self.path+filename+".png").convert()
				self.sprites[filename].set_colorkey((0, 0, 0))
			except:
				raise Exception(f"nao foi possivel carregar arquivo {self.path+filename+'.png'}")
		
		if rect:
			return self.sprites[filename].subsurface((rect[0]*8, rect[1]*8, rect[2]*8, rect[3]*8))
		return self.sprites[filename]