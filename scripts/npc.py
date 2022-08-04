from scripts.entidade import Entidade

class Npc(Entidade):
	def __init__(self, jogo, jsonData, dialogo):
		Entidade.__init__(self, jsonData["pos"][0], jsonData["pos"][1], jogo)
		self.dialogo = dialogo
		#sel.x, self.y = jsonData["pos"]
		self.loadAnimacoes(jsonData["sprite"])
		
	def loadAnimacoes(self, sprite):
		self.animacaoManager.load("andar baixo", "spritesheets/npcs", [0, 16*sprite], [16, 16], [32, 0], [0.25, 0.25])
		self.animacaoManager.load("andar direita", "spritesheets/npcs", [32, 16*sprite], [16, 16], [32, 0], [0.25, 0.25])
		self.animacaoManager.load("andar esquerda", "spritesheets/npcs", [64, 16*sprite], [16, 16], [32, 0], [0.25, 0.25])
		self.animacaoManager.load("andar cima", "spritesheets/npcs", [96, 16*sprite], [16, 16], [32, 0], [0.25, 0.25])
		self.animacaoManager.load("parado baixo", "spritesheets/npcs", [128, 16*sprite], [16, 16], [16, 0], [100])
		self.animacaoManager.load("parado direita", "spritesheets/npcs", [144, 16*sprite], [16, 16], [16, 0], [100])
		self.animacaoManager.load("parado esquerda", "spritesheets/npcs", [160, 16*sprite], [16, 16], [16, 0], [100])
		self.animacaoManager.load("parado cima", "spritesheets/npcs", [176, 16*sprite], [16, 16], [16, 0], [100])
		self.animacaoManager.ativar("parado esquerda")