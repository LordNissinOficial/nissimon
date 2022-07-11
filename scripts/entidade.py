from pygame import Rect


class Entidade():
	def __init__(self, x, y, largura, altura):
		self.largura = largura//8
		self.altura = altura//8
		self.x = x*8
		self.y = y*8
		self.xMovendo = x*8
		self.yMovendo = y*8
		self.movendo = [False, [0, 0]]
		self.dentroDeWarp = None #id do warp que usou para nao entrar num warp enquanto sai dele.
	
	def updateAnimacao(self):
		if self.movendo[0]:
			if self.movendo[1][0]==1 and self.animacaoManager.animacaoNome!="andar direita":
				self.animacaoManager.ativar("andar direita")
			elif self.movendo[1][0]==-1 and self.animacaoManager.animacaoNome!="andar esquerda":		
				self.animacaoManager.ativar("andar esquerda")
			elif self.movendo[1][1]==1 and self.animacaoManager.animacaoNome!="andar baixo":
				self.animacaoManager.ativar("andar baixo")
			elif self.movendo[1][1]==-1 and self.animacaoManager.animacaoNome!="andar cima":
				self.animacaoManager.ativar("andar cima")
		else:
			if self.movendo[1][0]==1 and self.animacaoManager.animacaoNome!="parado direita":
				self.animacaoManager.ativar("parado direita")
			elif self.movendo[1][0]==-1 and self.animacaoManager.animacaoNome!="parado esquerda":		
				self.animacaoManager.ativar("parado esquerda")
			elif self.movendo[1][1]==1 and self.animacaoManager.animacaoNome!="parado baixo":
				self.animacaoManager.ativar("parado baixo")
			elif self.movendo[1][1]==-1 and self.animacaoManager.animacaoNome!="parado cima":
				self.animacaoManager.ativar("parado cima")
				
	def mover(self, x, y, jogo, continuarMovendo=False):
		if not self.movendo[0]:
			self.movendo[1] = [x, y]
		if not self.podeMover(x, y, jogo):	return
		if self.movendo[0] and not continuarMovendo: return
		self.xMovendo = self.x
		self.yMovendo = self.y
		self.movendo[0] = True
		self.x += x*8
		self.y += y*8
	
	def podeMover(self, x, y, jogo):
		novoX = self.x//8+x
		novoY = self.y//8+y

		if 0<=novoX<len(jogo.mapaManager.grid[0][0])-self.largura+1 and 0<=novoY<len(jogo.mapaManager.grid[0])-self.altura+1:			
			for x in range(self.largura):
				for y in range(self.altura):					 
					 if jogo.mapaManager.colisoes[int(novoY+y)][int(novoX+x)]!=257:
					 	return False
			return True
		return False
	
	def updateMovimento(self, jogo, deltaTime):
		if self.movendo[0]:
			movendo = True
			#self.xMovendo += self.movendo[1][0]*48*deltaTime
#			self.yMovendo += self.movendo[1][1]*48*deltaTime
			self.xMovendo += self.movendo[1][0]
			self.yMovendo += self.movendo[1][1]
			if self.arrumarPosMovendo():
				self.movendo[0] = False
				self.xMovendo = self.x
				self.yMovendo = self.y
				
#				if self.emWarp(jogo):
#					self.movendo = [False, [0, 0]]
#					jogo.mapaManager.entrarWarp(Rect((self.x, self.y, self.largura*8, self.altura*8)))
#					self.x = 4*8
#					self.xMovendo = 4*8
#					self.y = 4*8
#					self.yMovendo = 4*8
				return 
				
			if self.xMovendo==self.x and self.yMovendo==self.y:
				continuarMovendo = False
				for index, botao in enumerate(["esquerda", "direita", "cima", "baixo"]):
					if [[-1, 0], [1, 0], [0, -1], [0, 1]][index]==self.movendo[1] and jogo.botoes[botao].pressionado:
						continuarMovendo = True
						break
				
				if self.emWarp(jogo):
						self.movendo = [False, [0, 0]]
						
						jogo.mapaManager.entrarWarp(Rect((self.x, self.y, self.largura*8, self.altura*8)))
						warp = jogo.mapaManager.funcoes[0]
						novoX, novoY = (warp.x, warp.y)#jogo.mapaManager.entrarWarp(Rect((self.x, self.y, self.largura*8, self.altura*8)))
						self.x = novoX
						self.xMovendo = novoX
						self.y = novoY
						self.yMovendo = novoY
#						self.x = novoX
#						self.xMovendo = novoX
#						self.y = novoY
#						self.yMovendo = novoY
						#self.x = 4*8
#						self.xMovendo = 4*8
#						self.y = 4*8
#						self.yMovendo = 4*8##fazer com que a posicao que acaba no novo mapa ea mesma que o warp
						
				if not continuarMovendo:					
					movendo = False
					self.movendo[0] = False
					self.xMovendo = self.x
					self.yMovendo = self.y
				else:
					self.mover(self.movendo[1][0], self.movendo[1][1], jogo, True)

	
	def arrumarPosMovendo(self):
		if self.movendo[1][0]==1 and self.xMovendo>self.x: return True
		if self.movendo[1][0]==-1 and self.xMovendo<self.x: return True
		if self.movendo[1][1]==1 and self.yMovendo>self.y: return True
		if self.movendo[1][1]==-1 and self.yMovendo<self.y: return True

	def emWarp(self, jogo):
		warp = jogo.mapaManager.emWarp(Rect(self.x, self.y, self.largura*8, self.altura*8))
		if warp:
			warpId = [propertie.value for propertie in warp.properties if propertie.name=="warp id"][0]
			if warpId==self.dentroDeWarp: return False
			self.dentroDeWarp = warpId
			return True
		else:
			self.dentroDeWarp = None
			return False