from pygame import event
from pygame import (Surface, image)
from pygame.font import (Font, init)
from pygame.transform import (scale, flip)
from pygame.locals import (QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP)
import copy, random, json
from enum import Enum
from scripts.nissimon import Nissimon
from scripts.transicao import (Transicao, TransicaoBatalha)
from scripts.uiComponentes import Botao
from scripts.inventario import Inventario
from scripts.spriteManager import SpriteManager
from scripts.spritesheet import SpriteSheet
from scripts.mapaManager import MapaManager
from scripts.camera import Camera
from scripts.jogador import Jogador
from scripts.config import *

init()

class CenaManager():
	
	"""classe principal que cuida do jogo atual"""	
	def __init__(self):
		self.estado = ESTADOS.OVERWORLD.value
		self.spriteManager = SpriteManager()
		self.transicao = Transicao()	
		self.transicaoBatalha = TransicaoBatalha()	
		self.estados = {estado: ESTADOS.estadosClasses.value[estado](self) for estado in ESTADOS.estados.value}
		for estado in self.estados:
			self.estados[estado].cenaManager = self

		self.rodando = 1
		self.eventos = []
		event.set_blocked(None)
		event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION])
		
	def fade(self, funcao=None):
		self.transicao = Transicao()
		if not self.transicao.fading:
			#self.fadeOutFuncao = funcao
			self.transicao.fadeOut(funcao)
			#self.transicao.fadeInFuncao = self.jogadorWarp
	def fadeBatalha(self):
		self.transicao = TransicaoBatalha()
		if not self.transicao.fading:
			#self.fadeOutFuncao = funcao
			self.transicao.fadeOut(lambda: self.setJogo(ESTADOS.BATALHA.value))
			
	def fadein(self):
		self.transicao.fadeIn()
		
	"""decide o jogo atual"""
	def setJogo(self, ESTADO):
		self.estado  = ESTADO#O.value
		#self.setUp()
		
	"""reinicia o jogo atual"""	
#	def setUp(self):
#		self.jogoAntigo = self.jogo
#		self.jogo = ESTADOS.estados.value[self.estado.value](self)
		
#		if self.jogoAntigo:
#			self.fade.fadeOut()
#		else:
#			self.jogo.setUp(self)
	"""updatea o jogo atual"""
	def update(self):
		if not self.rodando: return
		self.eventos = event.get()
		self.estados[self.estado].update(self)
		if self.transicao.fading:
			if self.transicao.fadeout:
				self.transicao.update()
				if self.transicao.fadein:
					#self.estados[self.estado].setUp(self)
					self.estados[self.estado].show()					
				return
			else:
				self.transicao.update()
		

	
	"""desenha na tela o display do jogo atual"""
	def show(self, tela):
		if not self.rodando: return
		self.estados[self.estado].show()
		if self.transicao.fading:			
			if self.transicao.fadeout:
				displayCopia = self.estados[self.estado].display.copy()
			else:
				self.estados[self.estado].show()
				displayCopia = self.estados[self.estado].display.copy()

			self.transicao.show(displayCopia)
			scale(displayCopia, TELA_TAMANHO, tela)
			return

		scale(self.estados[self.estado].display, TELA_TAMANHO, tela)

class Overworld():
	def __init__(self, cenaManager):
		self.spriteManager = cenaManager.spriteManager
		self.gramaBaixo = image.load("recursos/sprites/gramas/grama_baixo.png").convert()
		self.gramaBaixo.set_colorkey((100, 100, 100))
		#self.inventario = Inventario(self.spriteManager)
		self.spriteManager.load("spritesheets/ui")
		self.camera = Camera()
		
		self.jogador = Jogador(5, 14, self)
		#self.display = Surface([1920, 1080]).convert()
		self.gramas = []
		self.display = Surface((256, 144)).convert()
		self.mapaDisplay = Surface((DISPLAY_TAMANHO)).convert()
		self.mapaManager = MapaManager(self.camera)
		self.botoes = {}
		self.setUpBotoes(cenaManager)
	
	def setUpBotoes(self, cenaManager):
		botoes = self.botoes
		botoes["cima"] = Botao(16, DISPLAY_TAMANHO_REAL[1]-56, lambda: self.jogador.mover(0, -1, self), True)
		botoes["cima"].imgNormal = (4, 0, 2, 2)
		botoes["cima"].imgPressionando = (4, 2, 2, 2)
		
		botoes["baixo"] = Botao(16, DISPLAY_TAMANHO_REAL[1]-24, lambda: self.jogador.mover(0, 1, self), True)
		botoes["baixo"].imgNormal = (6, 0, 2, 2)
		botoes["baixo"].imgPressionando = (6, 2, 2, 2)
		
		botoes["esquerda"] = Botao(0, DISPLAY_TAMANHO_REAL[1]-40, lambda: self.jogador.mover(-1, 0, self), True)
		botoes["esquerda"].imgNormal = (0, 0, 2, 2)
		botoes["esquerda"].imgPressionando = (0, 2, 2, 2)
		
		botoes["direita"] = Botao(32, DISPLAY_TAMANHO_REAL[1]-40, lambda: self.jogador.mover(1, 0, self), True)
		botoes["direita"].imgNormal = (2, 0, 2, 2)
		botoes["direita"].imgPressionando = (2, 2, 2, 2)

	def fade(self, funcao=None):
		self.cenaManager.fade(lambda: self.jogadorWarp(funcao))
	
	def fadein(self):
		self.cenaManager.fadein(self.jogadorWarp)
		print(3333)
#	
	def fadeBatalha(self):
		self.cenaManager.fadeBatalha()
		
	def jogadorWarp(self, funcao):
		funcao()
		warp = self.mapaManager.mapas["centro"].funcoes[0]
		novoX, novoY = (warp.x, warp.y)
		self.jogador.x = novoX
		self.jogador.xMovendo = novoX
		self.jogador.y = novoY
		self.jogador.yMovendo = novoY
		self.jogador.andarAutomatico = 5
		
	def update(self, cenaManager):
		for botao in self.botoes:
			if cenaManager.transicao.fading: break
			self.botoes[botao].update()
		
		if not cenaManager.transicao.fading:
			
			self.jogador.update(self)
		else:
			self.jogador.movendo[0] = False
			self.jogador.x = self.jogador.xMovendo
			self.jogador.y = self.jogador.yMovendo
		self.camera.moverPara(self.jogador.xMovendo, self.jogador.yMovendo, self.mapaManager.mapas['centro'])
		
		self.mapaManager.updateAnimacoes(self.camera)
		self.lidarEventos(cenaManager)
	
	def checarGrama(self, x, y):
		#print(self.mapaManager.mapas["centro"].grid[0], x//16, y//16)
		if self.mapaManager.mapas["centro"].grid[0][y//16][x//16]==25:
			#print(5555)
			if random.randint(1, 100)<=100:
				self.fadeBatalha()
#		if self.mapaManager
#		self.gramas.append([x,  y+4])
		
	def show(self):
		
		if self.camera.mudouPosicao():
			self.mapaManager.updateDisplay(self.camera)

		self.mapaManager.show(self.mapaDisplay)
		self.jogador.show(self.mapaDisplay, self.camera, self.mapaManager.mapas["centro"].offsetX, self.mapaManager.mapas["centro"].offsetY)
		
		self.display.blit(self.mapaDisplay, (0, 0))
		for grama in self.gramas:
			pos = [grama[0]-self.camera.x, grama[1]-self.camera.y]
			self.display.blit(self.gramaBaixo, (pos))
			#print(grama[1], pos)
#			self.display.set_at(pos, grama[0])
#			grama[1][1] += 1
#			grama[2] -= random.randint(0, 1)
#			if grama[2]<=0:
				
			#print(grama[1])
			self.gramas.remove(grama)
		self.showUi()
	
	def showUi(self):
		for botao in self.botoes:
			self.botoes[botao].show(self.display, self.spriteManager)

	def lidarEventos(self, cenaManager):
		for evento in cenaManager.eventos:			
			if evento.type in [MOUSEBUTTONDOWN, MOUSEMOTION]:
				pos = telaParaDisplay(*evento.pos)
				for botao in self.botoes:
					self.botoes[botao].pressionandoMouse(pos)
				
			elif evento.type==MOUSEBUTTONUP:
				pos = telaParaDisplay(*evento.pos)
				for botao in self.botoes:
					self.botoes[botao].tirandoMouse(pos)

class Batalha():
	def __init__(self, cenaManager):
		self.display = Surface(DISPLAY_TAMANHO).convert()
		self.fonte = Font("recursos/sprites/fonte.ttf", 8)
		self.nissimonData = json.load(open("recursos/data/nissimons.json", "r"))
		self.botoes = image.load("recursos/sprites/batalha_botoes.png").convert()
		self.nissimonUi1 = image.load("recursos/sprites/nissimon_ui.png").convert()
		self.nissimonUi2 = flip(self.nissimonUi1, True, False)
		self.nissimon1 = Nissimon(self.nissimonData["charmander"])
		self.nissimon2 = Nissimon(self.nissimonData["charmander"])
		self.sprite1 = image.load("recursos/sprites/nissimons/costas.png").convert()
		self.sprite2 = image.load("recursos/sprites/nissimons/frente.png").convert()

	def update(self, cenaManager):
		pass
	
	def show(self):
		self.display.fill((255, 255, 255))
		self.display.blit(self.sprite1, (16, 144-46-56))
		self.display.blit(self.sprite2, (256-56-16, 8))
		self.display.blit(self.botoes, (8, 144-45))
		self.display.blit(self.nissimonUi1, (256-96, 144-45-40))
		self.display.blit(self.fonte.render(self.nissimon1.nome, 0, (0, 0, 0), (255, 255, 255)), (256-92, 144-45-38))
		self.display.blit(self.fonte.render(f"LV.{self.nissimon1.level}", 0, (0, 0, 0), (255, 255, 255)), (256-92, 144-45-24+3))
		
		self.display.blit(self.nissimonUi2, (8, 25))
		self.display.blit(self.fonte.render(self.nissimon2.nome, 0, (0, 0, 0), (255, 255, 255)), (14, 45-18))
		self.display.blit(self.fonte.render(f"LV.{self.nissimon2.level}", 0, (0, 0, 0), (255, 255, 255)), (14, 44))
		
class ESTADOS(Enum):
	OVERWORLD = 0
	BATALHA = 1
	MENUPRINCIPAL = 2
	estados = [OVERWORLD, BATALHA]#, MENUPRINCIPAL
	estadosClasses = [Overworld, Batalha]#MenuPrincipal, MenuConfiguracoes]
	
def telaParaDisplay(x, y):
	return [int(x/TELA_TAMANHO[0]*DISPLAY_TAMANHO_REAL[0]),
				int(y/TELA_TAMANHO[1]*DISPLAY_TAMANHO_REAL[1])]