from pygame import Rect


class Entidade():
	def __init__(self, x, y, largura, altura):
		self.andarAutomatico = 0
		self.largura = largura//16
		self.moverCount = 0
		self.altura = altura//16
		self.x = x*16
		self.y = y*16
		self.xMovendo = x*16
		self.mm = False
		self.yMovendo = y*16
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
		if not self.movendo[0] and (x!=self.movendo[1][0] or y!=self.movendo[1][1]):
			self.movendo[1] = [x, y]
			self.moverCount = 5
			return
		
		if self.moverCount>0:
			self.moverCount-=1
			return

		if self.andarAutomatico>0: return
		if not self.movendo[0]:
			self.movendo[1] = [x, y]
		if not self.podeMover(x, y, jogo):	return
		if self.movendo[0] and not continuarMovendo: return
		self.xMovendo = self.x
		self.yMovendo = self.y
		self.movendo[0] = True
		self.x += x*16
		self.y += y*16
	
	def podeMover(self, x, y, jogo):
		novoX = self.x//16+x
		novoY = self.y//16+y

		if 0<=novoX<len(jogo.mapaManager.colisoes[0])-self.largura+1 and 0<=novoY<len(jogo.mapaManager.colisoes)-self.altura+1:			

			if jogo.mapaManager.colisoes[int(novoY)][int(novoX)]!=65:
				return False
			return True
		return False
	
	def m(self):
		self.mm = not self.mm
		
	def updateMovimento(self, jogo):
		if self.andarAutomatico>0:
			self.andarAutomatico -= 1
			if self.andarAutomatico==0:
				self.mover(self.movendo[1][0], self.movendo[1][1], jogo)
		if self.movendo[0]:
			movendo = True
			self.xMovendo += self.movendo[1][0]
			self.yMovendo += self.movendo[1][1]
			if self.arrumarPosMovendo():
				self.movendo[0] = False
				self.xMovendo = self.x
				self.yMovendo = self.y
				return 
				
			if self.xMovendo==self.x and self.yMovendo==self.y:
				continuarMovendo = False
				for index, botao in enumerate(["esquerda", "direita", "cima", "baixo"]):
					if [[-1, 0], [1, 0], [0, -1], [0, 1]][index]==self.movendo[1] and jogo.botoes[botao].pressionado:
						continuarMovendo = True
						break
				
				
					
				if self.emWarp(jogo, (self.x, self.y, self.largura*16, self.altura*16)):
						self.movendo[0] = False					
						jogo.mapaManager.entrarWarp(Rect((self.x, self.y, self.largura*8, self.altura*8)), jogo)
#						warp = jogo.mapaManager.funcoes[0]
#						novoX, novoY = (warp.x, warp.y)
#						self.x = novoX
#						self.xMovendo = novoX
#						self.y = novoY
#						self.yMovendo = novoY
#						self.andarAutomatico = 5
#			elif self.movendo[0] and self.emWarp(jogo, (self.x, self.y, 16, 16), False):

#					jogo.fade()
#						self.x = novoX
#						self.xMovendo = novoX
#						self.y = novoY
#						self.yMovendo = novoY
						#self.x = 4*8
#						self.xMovendo = 4*8
#						self.y = 4*8
#						self.yMovendo = 4*8##fazer com que a posicao que acaba no novo mapa ea mesma que o warp
						
		#		if not continuarMovendo:					
#					movendo = False
#					self.movendo[0] = False
#					self.xMovendo = self.x
#					self.yMovendo = self.y
#				else:
#					self.mover(self.movendo[1][0], self.movendo[1][1], jogo, True)

	
	def arrumarPosMovendo(self):
		if self.movendo[1][0]==1 and self.xMovendo>self.x: return True
		if self.movendo[1][0]==-1 and self.xMovendo<self.x: return True
		if self.movendo[1][1]==1 and self.yMovendo>self.y: return True
		if self.movendo[1][1]==-1 and self.yMovendo<self.y: return True

	def emWarp(self, jogo, rect, entrar=True):
		warp = jogo.mapaManager.emWarp(Rect(rect))
		if warp:
			warpId = [propertie.value for propertie in warp.properties if propertie.name=="warp id"][0]
			if entrar:
				if warpId==self.dentroDeWarp: return False
				self.dentroDeWarp = warpId
			return True
		else:
			self.dentroDeWarp = None
			return False