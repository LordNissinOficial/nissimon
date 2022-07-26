from pygame import event
from pygame import Surface
from pygame.transform import scale
from pygame.locals import (QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP)
import pickle, copy
from enum import Enum
from scripts.transicao import Transicao
from scripts.uiComponentes import Botao
from scripts.inventario import Inventario
from scripts.spriteManager import SpriteManager
from scripts.spritesheet import SpriteSheet
from scripts.mapaManager import MapaManager
from scripts.camera import Camera
from scripts.jogador import Jogador
from scripts.config import *

class CenaManager():
	
	"""classe principal que cuida do jogo atual"""	
	def __init__(self):
		self.estado = ESTADOS.OVERWORLD.value
		self.spriteManager = SpriteManager()
		self.transicao = Transicao()
		
		self.estados = {estado: ESTADOS.estadosClasses.value[estado](self) for estado in ESTADOS.estados.value}
		for estado in self.estados:
			self.estados[estado].cenaManager = self

		self.rodando = 1
		self.eventos = []
		event.set_blocked(None)
		event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION])
		
	def fade(self, funcao=None):
		if not self.transicao.fading:
			#self.fadeOutFuncao = funcao
			self.transicao.fadeOut(funcao)
			#self.transicao.fadeInFuncao = self.jogadorWarp
			
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
		#self.inventario = Inventario(self.spriteManager)
		self.spriteManager.load("spritesheets/ui")
		self.camera = Camera()
		
		self.jogador = Jogador(5, 5, self)
		#self.display = Surface([1920, 1080]).convert()
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
			self.botoes[botao].update()
			
		self.jogador.update(self)
		self.camera.moverPara(self.jogador.xMovendo, self.jogador.yMovendo, self.mapaManager.mapas['centro'])
		self.mapaManager.updateAnimacoes(self.camera)
		self.lidarEventos(cenaManager)

	def show(self):
		if self.camera.mudouPosicao():
			self.mapaManager.updateDisplay(self.camera)

		self.mapaManager.show(self.mapaDisplay)
		self.jogador.show(self.mapaDisplay, self.camera, self.mapaManager.mapas["centro"].offsetX, self.mapaManager.mapas["centro"].offsetY)
		self.display.blit(self.mapaDisplay, (0, 0))
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
		
class ESTADOS(Enum):
	OVERWORLD = 0
	INVENTARIO = 1
	MENUPRINCIPAL = 2
	MENUCONFIGURACOES = 3
	MENUAJUDA = 4
	estados = [OVERWORLD, INVENTARIO]#, MENUPRINCIPAL
	estadosClasses = [Overworld, Inventario]#MenuPrincipal, MenuConfiguracoes]
	
def telaParaDisplay(x, y):
	return [int(x/TELA_TAMANHO[0]*DISPLAY_TAMANHO_REAL[0]),
				int(y/TELA_TAMANHO[1]*DISPLAY_TAMANHO_REAL[1])]