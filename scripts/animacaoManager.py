from time import time
from copy import copy
from scripts.animacao import Animacao

class AnimacaoManager:
	def __init__(self, spriteManager):
		self.spriteManager = spriteManager
		self.animacoes = {}
		self.animacaoAtual = None
		self.animacaoNome = None
		
	def load(self, animacaoNome, filename, comeco, tileTamanho, rect, duracoes):
		self.animacoes[animacaoNome] = Animacao(filename, comeco, tileTamanho, rect, duracoes)
		
	def ativar(self, animacaoNome):
		self.animacaoAtual = copy(self.animacoes[animacaoNome])
		self.animacaoNome = animacaoNome
		
	def update(self):
		if self.animacaoAtual and self.animacaoAtual.podeUpdatear(time()):
			self.animacaoAtual.update()
		
	def conseguirSprite(self):
		if not self.animacaoAtual: return pg.Surface((100, 150, 200))
		return self.animacaoAtual.conseguirSprite(self.spriteManager)