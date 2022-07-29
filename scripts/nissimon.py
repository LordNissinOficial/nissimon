from random import randint
class Nissimon:
	def __init__(self, jsonData):
		self.hp = jsonData["hp"]
		self.hpMaximo  = self.hp
		self.ataque = jsonData["ataque"]
		self.ataqueEspecial = jsonData["ataque especial"]
		self.defesa = jsonData["defesa"]
		self.defesaEspecial = jsonData["defesa especial"]
		self.velocidade = jsonData["velocidade"]
		self.ataques = jsonData["ataques"]
		self.nome = jsonData["nome"]
		self.level = randint(jsonData["level"][0], jsonData["level"][1])
		self.condicao = 0
	