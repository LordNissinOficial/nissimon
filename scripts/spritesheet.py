from pygame.image import load as loadImage

class SpriteSheet():
	def __init__(self, filename):
		self.sprite = loadImage("recursos/sprites/"+filename+".png").convert_alpha()
		#self.path = "recursos/sprites/"
	
	def m(self, filename):
		self.sprite = loadImage("recursos/sprites/"+filename+".png").convert_alpha()
		
	def load(self, x, y, largura, altura):
		return self.sprite.subsurface((x*8, y*8, largura*8, altura*8))
		#if filename not in self.sprites.keys():
#			self.sprites[filename] = loadImage(self.path+filename+".png")
#		return self.sprites[filename].subsurface((x*8, y*8, largura*8, altura*8))