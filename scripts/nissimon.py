from random import randint
class Nissimon:
	def __init__(self, jsonData):
		self.tipos = jsonData["tipos"]
		self.stats = jsonData["stats"]
		self.hp = self.stats[0]
		self.ataques = jsonData["ataques"]
		self.nome = jsonData["nome"]
		self.level = randint(jsonData["level"][0], jsonData["level"][1])
		self.condicao = 0
		self.xp = 0
		self.xpMaximo = 100
	