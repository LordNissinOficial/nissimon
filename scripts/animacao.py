class Animacao:
	def __init__(self, filename, comeco, tileTamanho, rect, duracoes):
		self.comeco = comeco
		self.filename = filename
		self.tileTamanho = tileTamanho
		self.rect = rect
		duracoes = duracoes
		self.spriteAtual = 0
		self.spriteMaximo = rect[0]//tileTamanho[0]
		self.tempoAntigo = None
		
	def update(self):
		self.spriteAtual += tileTamanho[0]
		if self.spriteAtual>self.spriteMaximo:
			self.spriteAtual = 0
	
	def podeUpdatear(self, tempo):
		if not tempoAntigo: return False
		return tempo-self.tempoAntigo>=self.duracoes[self.spriteAtual//tileTamanho[0]]
	
	def conseguirSprite(self, spriteManager):
		return spriteManager.load(self.filename, (self.comeco[0]+self.spriteAtual, self.comeco[1], self.tileTamanho[0], self.tileTamanho[1]))