from scripts.entidade import Entidade
from scripts.animacaoManager import AnimacaoManager

class Jogador(Entidade):
	def __init__(self, x, y, jogo):
		Entidade.__init__(self, x, y)
		self.animacaoManager = AnimacaoManager(jogo.spriteManager)
		self.animacaoManager.load("andar baixo", "spritesheets/jogador", [0, 0], [16, 16], [32, 0], [0.25, 0.25])
		self.animacaoManager.load("andar direita", "spritesheets/jogador", [32, 0], [16, 16], [32, 0], [0.25, 0.25])
		self.animacaoManager.load("andar esquerda", "spritesheets/jogador", [64, 0], [16, 16], [32, 0], [0.25, 0.25])
		self.animacaoManager.load("andar cima", "spritesheets/jogador", [96, 0], [16, 16], [32, 0], [0.25, 0.25])
		self.animacaoManager.load("parado baixo", "spritesheets/jogador", [0, 16], [16, 16], [16, 0], [100])
		self.animacaoManager.load("parado direita", "spritesheets/jogador", [16, 16], [16, 16], [16, 0], [100])
		self.animacaoManager.load("parado esquerda", "spritesheets/jogador", [32, 16], [16, 16], [16, 0], [100])
		self.animacaoManager.load("parado cima", "spritesheets/jogador", [48, 16], [16, 16], [16, 0], [100])
		self.animacaoManager.ativar("parado baixo")
		self.eJogador = True
		
	def update(self, jogo):
		self.updateAnimacao()
		self.animacaoManager.update()
		self.updateMovimento(jogo)

	def show(self, display, camera, offsetX, offsetY):
		x = self.xMovendo-camera.x
		y = self.yMovendo-camera.y-4
		display.blit(self.animacaoManager.conseguirSprite(), (x, y))