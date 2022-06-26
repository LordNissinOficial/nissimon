from time import time
from copy import copy
from scripts.animacao import Animacao

class AnimacaoManager:
	def __init__(self, spriteManager):
		self.spriteManager = spriteManager
		self.animacoes = {}
		self.animacaoAtual
		
	def loadAnimacao(animacaoNome, filename, comeco, tileTamanho, rect, duracoes):
		self.animacoes[animacaoNome] = Animacao(animacaoNome, filename, comeco, tileTamanho, rect, duracoes)
	
	def ativarAnimacao(self, animacaoNome):
		self.animacaoAtual = copy(self.animacoes[animacaoNome])
	
	def update(self):
		if self.animacaoAtual.podeUpdatear(time()):
			self.animacaoAtual.update()
	
	def conseguirSprite(self):
		return self.animacaoAtual.conseguirSprite(self.spriteManager)