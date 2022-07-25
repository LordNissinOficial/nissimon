from pygame.image import load as loadImage
from pygame.locals import RLEACCEL
from pygame.font import (init, Font)
from functools import cache
from scripts.config import FUNDO_SPRITESHEET

init()

class SpriteManager():
	def __init__(self):
		self.path = "recursos/sprites/"
		self.spriteAtual = None
		self.fonte = Font("recursos/alagard.ttf", 16)
		self.sprites = {}
		self.fontes = {}
	
	def underline(bool):
		self.fonte.set_underline(bool)

	@cache
	def load(self, filename, rect=None):
		if filename not in self.sprites:
			try:
				self.sprites[filename] = loadImage(self.path+filename+".png").convert()
				self.sprites[filename].set_colorkey(FUNDO_SPRITESHEET)
			except:
				raise Exception(f"nao foi possivel carregar arquivo {self.path+filename+'.png'}")
		
		if rect:
			return self.sprites[filename].subsurface((rect[0]*8, rect[1]*8, rect[2]*8, rect[3]*8))
		return self.sprites[filename]