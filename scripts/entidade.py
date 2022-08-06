from pygame import Rect
from scripts.animacaoManager import AnimacaoManager

class Entidade():
	def __init__(self, x, y, jogo):
		self.animacaoManager = AnimacaoManager(jogo.spriteManager)

		self.eJogador = False
		self.andarAutomatico = 0
		self.largura = 1
		self.moverCount = 0
		self.altura = 1
		self.x = x*16
		self.y = y*16
		self.xMovendo = x*16
		self.mm = False
		self.yMovendo = y*16
		self.movendo = [False, [0, 1]]
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
		if self.andarAutomatico>0: return
		if not self.movendo[0] and (x!=self.movendo[1][0] or y!=self.movendo[1][1]):
			self.movendo[1] = [x, y]
			self.moverCount = 10
			return
		
		if self.moverCount>0:
			self.moverCount-=1
			return

		
		if not self.movendo[0]:
			self.movendo[1] = [x, y]
		
		if self.movendo[0] and not continuarMovendo: return
		podeMover = self.podeMover(x, y, jogo)
		if not podeMover:	return
		
		if self.eJogador:
			if podeMover[1]=="cima":
				self.xMovendo = self.x
				self.yMovendo = len(jogo.mapaManager.mapas["centro"].colisoes)*16
				self.movendo[0] = True
				self.x += x*16
				self.y = len(jogo.mapaManager.mapas["centro"].colisoes)*16-16
			elif podeMover[1]=="baixo":
				self.xMovendo = self.x
				self.yMovendo = -16
				self.movendo[0] = True
				self.x += x*16
				self.y = 0
			elif podeMover[1]=="esquerda":
				self.xMovendo = len(jogo.mapaManager.mapas["centro"].colisoes[0])*16
				self.yMovendo = self.y
				self.movendo[0] = True
				self.x = len(jogo.mapaManager.mapas["centro"].colisoes[0])*16-16
				self.y += y*16
			elif podeMover[1]=="direita":
				self.xMovendo = -16
				self.yMovendo = self.y
				self.movendo[0] = True
				self.x = 0
				self.y += y*16	
			elif podeMover[1]=="centro":
				self.xMovendo = self.x
				self.yMovendo = self.y
				self.movendo[0] = True
				self.x += x*16
				self.y += y*16
		else:
			print("se ferro")
#			self.xMovendo = self.x
#			self.yMovendo = self.y
#			self.movendo[0] = True
#			self.x += x*16
#			self.y += y*16
	
	def podeMover(self, x, y, jogo):
		novoX = self.x//16+x
		novoY = self.y//16+y
		
		return jogo.mapaManager.podeMover(novoX, novoY, self.eJogador)

	def updateMovimento(self, jogo):
		if self.andarAutomatico>0:
			self.andarAutomatico -= 1
			if self.andarAutomatico==0:
				self.mover(self.movendo[1][0], self.movendo[1][1], jogo)
		if self.movendo[0]:
			
			movendo = True
			self.xMovendo += self.movendo[1][0]
			self.yMovendo += self.movendo[1][1]

			if self.xMovendo==self.x and self.yMovendo==self.y:
				self.movendo[0] = False
				jogo.checarGrama(self.x, self.y)
				if self.emWarp(jogo, (self.x, self.y, self.largura*16, self.altura*16)):
						self.movendo[0] = False					
						jogo.mapaManager.entrarWarp(Rect((self.x, self.y, self.largura*8, self.altura*8)), jogo)

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
				
	def update(self, jogo):
		self.updateAnimacao()
		self.animacaoManager.update()
		self.updateMovimento(jogo)

	def show(self, display, camera, offsetX, offsetY):
		x = self.xMovendo-camera.x
		y = self.yMovendo-camera.y-4
		display.blit(self.animacaoManager.conseguirSprite(), (x, y))