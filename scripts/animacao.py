class Animacao:
	def __init__(self, filename, comeco, tileTamanho, rect, duracoes):
		self.comeco = comeco
		self.filename = filename
		self.tileTamanho = tileTamanho
		self.rect = rect
		self.duracoes = duracoes
		self.spriteAtual = 0
		self.spriteMaximo = rect[0]
		self.tempoAntigo = None
		
	def update(self):
		self.spriteAtual += self.tileTamanho[0]
		if self.spriteAtual>=self.spriteMaximo:
			self.spriteAtual = 0

	def podeUpdatear(self, tempo):
		if not self.tempoAntigo:
			self.tempoAntigo = tempo
		if tempo-self.tempoAntigo>=self.duracoes[self.spriteAtual//self.tileTamanho[0]]:
			self.tempoAntigo = tempo
			return True
	
	def conseguirSprite(self, spriteManager):
		return spriteManager.load(self.filename, ((self.comeco[0]+self.spriteAtual)//8, (self.comeco[1])//8, self.tileTamanho[0]//8, self.tileTamanho[1]//8))