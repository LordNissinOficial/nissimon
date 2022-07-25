from pygame import (Surface, transform, draw)
from scripts.config import *


class Transicao:
	def __init__(self):
		self.fadeout = False
		self.fadein = False
		self.fading = False
		self.largura = 32
		self.altura = 16
		self.alpha = 255
		self.pause = 2
		self.maxArea = self.largura*1.1
		self.area = self.maxArea		
		self.fade = Surface((self.largura, self.altura)).convert()
		self.funcao = None
		#self.funcaoFadeIn = 
			
	def fadeOut(self, funcao=None):
		self.pause = 2
		self.funcao = funcao
		self.fadeout = True
		self.alpha = 0
		self.fadein = False
		self.fading = True
	
	def fadeIn(self):
		self.fadeout = False
		self.fadein = True
		self.fading = True
		
	def update(self):
		
		if self.fadeout:			
			self.alpha += 40
			
			if self.alpha>255:
				self.pause -= 1
				if self.pause>0: return
				self.pause = 2
				if self.funcao!=None:
					self.funcao()
				self.alpha = 255
				self.fadeout = False
				self.fadein = True
				
			return
#		if self.area
		self.alpha -= 40

		if self.alpha<0:
			self.alpha = 0
			self.fadein = False
			self.fading = False

	def show(self, screen):
		fade = Surface((1, 1)).convert()
		self.fade.fill((255, 255, 255))
		#self.fade.fill(TRANSITION_COLOR)
		#draw.circle(self.fade, (24, 24, 24), (self.largura/2, self.altura/2), self.area)
		#self.fade.set_colorkey((24, 24, 24))
		self.fade.set_alpha(self.alpha)
		screen.blit(transform.scale(self.fade, screen.get_size()), (0, 0))

