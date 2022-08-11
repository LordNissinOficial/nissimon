from pygame import event
from pygame import (Surface, image, draw)
from pygame.font import (Font, init)
from pygame.transform import (scale, flip)
from pygame.locals import (QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP)
import copy, random, json
from enum import Enum
from scripts.nissimon import Nissimon
from scripts.transicao import (Transicao, TransicaoBatalha)
from scripts.uiComponentes import Botao
from scripts.inventario import Inventario
from scripts.dialogoManager import DialogoManager
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
		self.nissimonData = json.load(open("recursos/data/nissimons.json", "r"))
		self.movimentosData = json.load(open("recursos/data/movimentos.json", "r"))
		self.party = [Nissimon(self.nissimonData["charmander"])]
		self.botoes = {}
		self.setBotoes() 
		self.spriteManager = SpriteManager()
		self.transicao = Transicao()	
		self.transicaoBatalha = TransicaoBatalha()	
		self.estados = {estado: ESTADOS.estadosClasses.value[estado](self) for estado in ESTADOS.estados.value}
		for estado in self.estados:
			self.estados[estado].cenaManager = self
		self.setJogo(ESTADOS.OVERWORLD)
		self.rodando = 1
		event.set_blocked(None)
		event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION])

	def setBotoes(self):
		botoes = self.botoes
		botoes["cima"] = Botao(16+4, DISPLAY_TAMANHO_REAL[1]-56+4)
		botoes["cima"].imgNormal = (4, 0, 2, 2)
		botoes["cima"].imgPressionando = (4, 2, 2, 2)
		
		botoes["baixo"] = Botao(16+4, DISPLAY_TAMANHO_REAL[1]-24+4)
		botoes["baixo"].imgNormal = (6, 0, 2, 2)
		botoes["baixo"].imgPressionando = (6, 2, 2, 2)
		
		botoes["esquerda"] = Botao(4, DISPLAY_TAMANHO_REAL[1]-40+4)
		botoes["esquerda"].imgNormal = (0, 0, 2, 2)
		botoes["esquerda"].imgPressionando = (0, 2, 2, 2)
		
		botoes["direita"] = Botao(32+4, DISPLAY_TAMANHO_REAL[1]-40+4)
		botoes["direita"].imgNormal = (2, 0, 2, 2)
		botoes["direita"].imgPressionando = (2, 2, 2, 2)
		
		botoes["b"] = Botao(DISPLAY_TAMANHO[0]-32-14, DISPLAY_TAMANHO_REAL[1]-24+4)
		botoes["b"].imgNormal = (8, 0, 2, 2)
		botoes["b"].imgPressionando = (8, 2, 2, 2)
		
		botoes["a"] = Botao(DISPLAY_TAMANHO[0]-16-4, DISPLAY_TAMANHO_REAL[1]-24+4)
		botoes["a"].imgNormal = (10, 0, 2, 2)
		botoes["a"].imgPressionando = (10, 2, 2, 2)
		
	def fade(self, funcao=None):
		for botao in self.botoes:
			self.botoes[botao].pressionado = False
		self.transicao = Transicao()
		if not self.transicao.fading:
			self.transicao.fadeOut(funcao)

	def fadeBatalha(self):
		self.transicao = TransicaoBatalha()
		if not self.transicao.fading:
			self.transicao.fadeOut(lambda: self.setJogo(ESTADOS.LUTA))
			
	def fadein(self):
		self.transicao.fadeIn()
		
	"""decide o jogo atual"""
	def setJogo(self, ESTADO):
		self.estado  = ESTADO.value
		self.estados[self.estado].setUp(self)
		for botao in self.botoes:
			self.botoes[botao].pressionado = False
	
	def lidarEventos(self):
		for evento in event.get():
			if evento.type==QUIT:
				self.rodando = False
			elif evento.type in [MOUSEBUTTONDOWN, MOUSEMOTION] and not self.transicao.fading:
				pos = telaParaDisplay(*evento.pos)
				for botao in self.botoes:
					self.botoes[botao].pressionandoMouse(pos)
				
			elif evento.type==MOUSEBUTTONUP and not self.transicao.fading:
				pos = telaParaDisplay(*evento.pos)
				for botao in self.botoes:
					self.botoes[botao].tirandoMouse(pos)
					
	"""updatea o jogo atual"""
	def update(self):
		if not self.rodando: return
		self.lidarEventos()
		self.estados[self.estado].update(self)
		if self.transicao.fading:
			if self.transicao.fadeout:
				self.transicao.update()
				if self.transicao.fadein:
					self.estados[self.estado].show()					
				return
			else:
				self.transicao.update()
		else:
			for botao in self.botoes:
				self.botoes[botao].update()

	
	"""desenha na tela o display do jogo atual"""
	def show(self, tela):
		if not self.rodando: return
		self.estados[self.estado].show()
		self.showUi()
		if self.transicao.fading:			
			if self.transicao.fadeout:
				displayCopia = self.estados[self.estado].display.copy()
			else:
				self.estados[self.estado].show()
				self.showUi()
				displayCopia = self.estados[self.estado].display.copy()

			self.transicao.show(displayCopia)
			scale(displayCopia, TELA_TAMANHO, tela)
			return

		scale(self.estados[self.estado].display, TELA_TAMANHO, tela)
	
	def showUi(self):
		for botao in self.botoes:
			self.botoes[botao].show(self.estados[self.estado].display, self.spriteManager)
			
class Overworld():
	def __init__(self, cenaManager):
		self.spriteManager = cenaManager.spriteManager
		self.dialogoManager = DialogoManager()
		self.gramaBaixo = image.load("recursos/sprites/gramas/grama_baixo.png").convert()
		self.gramaBaixo.set_colorkey((100, 100, 100))
		self.spriteManager.load("spritesheets/ui")
		self.camera = Camera()	
		self.jogador = Jogador(3, 4, self)
		self.gramas = []
		self.display = Surface((256, 144)).convert()
		self.mapaDisplay = Surface((DISPLAY_TAMANHO)).convert()
		self.mapaManager = MapaManager(self.camera,  self)
		self.botoes = {}
	
	def setUp(self, cenaManager):
		self.setUpBotoes(cenaManager)
		
	def setUpBotoes(self, cenaManager):
		cenaManager.botoes["cima"].setFuncao(lambda: self.moverJogador(0, -1), True)
		cenaManager.botoes["baixo"].setFuncao(lambda: self.moverJogador(0, 1), True)
		cenaManager.botoes["esquerda"].setFuncao(lambda: self.moverJogador(-1, 0), True)
		cenaManager.botoes["direita"].setFuncao(lambda: self.moverJogador(1, 0), True)
		
		cenaManager.botoes["b"].setFuncao(None, False)
		cenaManager.botoes["a"].setFuncao(self.a, False)
		cenaManager.botoes["a"].setFuncaoSolto(self.aSolto)
	
	def moverJogador(self, x, y):
		if self.dialogoManager.emDialogo: return
		self.jogador.mover(x, y, self)
		
	def a(self):
		if self.dialogoManager.emDialogo:
			dialogoMng = self.dialogoManager
			if (dialogoMng.visivel[0]+1)%2==0 and dialogoMng.visivel[1]==len(dialogoMng.texto[dialogoMng.visivel[0]])-1:
				if dialogoMng.visivel[0]+1<len(dialogoMng.texto):
					dialogoMng.visivel[0] += 1
					dialogoMng.visivel[1] = 0
			if dialogoMng.visivel[0]==len(dialogoMng.texto)-1 and dialogoMng.visivel[1]==len(dialogoMng.texto[dialogoMng.visivel[0]])-1 and dialogoMng.acabarTimer==0:
				dialogoMng.emDialogo = False
			else:
				self.dialogoManager.timerTanto = 0
		elif self.mapaManager.olhandoParaNpc(self.jogador):
			self.dialogoManager.comecarDialogo(self.mapaManager.conseguirNpcDialogo(self.jogador))
	
	def aSolto(self):
		if self.dialogoManager.emDialogo:
			self.dialogoManager.timerTanto = 1
			
	def fade(self, funcao, warp):
		self.cenaManager.fade(lambda: self.jogadorWarp(funcao, warp))
	
	def fadein(self):
		self.cenaManager.fadein(self.jogadorWarp)

	def fadeBatalha(self):
		self.cenaManager.fadeBatalha()
		
	def jogadorWarp(self, funcao, warpId):
		funcao()
		for funcao in self.mapaManager.mapas["centro"].funcoes:
			if funcao.type=="warp":
				for propriedade in funcao.properties:
					if propriedade.name=="id" and propriedade.value==warpId:
						warp = funcao
						break
		for propriedade in warp.properties:
			if propriedade.name=="direcao":
				direcao = list(map(int, propriedade.value.split(",")))

		novoX, novoY = (warp.x, warp.y)
		self.jogador.x = novoX
		self.jogador.xMovendo = novoX
		self.jogador.y = novoY
		self.jogador.yMovendo = novoY
		self.jogador.movendo[1] = direcao
		self.jogador.updateAnimacao()
		self.jogador.andarAutomatico = 1
		
	def update(self, cenaManager):

		if not cenaManager.transicao.fading:
			self.jogador.update(self)
			self.mapaManager.update(self)
			if self.dialogoManager.emDialogo:
				self.dialogoManager.update()
			
		else:
			self.jogador.movendo[0] = False
			self.jogador.x = self.jogador.xMovendo
			self.jogador.y = self.jogador.yMovendo
		self.camera.moverPara(self.jogador.xMovendo, self.jogador.yMovendo, self.mapaManager.mapas['centro'])
		
		self.mapaManager.updateAnimacoes(self.camera)
	
	def checarGrama(self, x, y):
		if self.mapaManager.mapas["centro"].grid[0][y//16][x//16]==25:
			if random.randint(1, 100)<=15:
				self.fadeBatalha()

	def show(self):		
		if self.camera.mudouPosicao() or True:
			self.mapaManager.updateDisplay(self.camera)

		self.mapaManager.show(self.display)
		self.jogador.show(self.display, self.camera, self.mapaManager.mapas["centro"].offsetX, self.mapaManager.mapas["centro"].offsetY)

		if self.dialogoManager.emDialogo:
			self.dialogoManager.show(self.display)

class Luta():
	def __init__(self, cenaManager):
		self.display = Surface(DISPLAY_TAMANHO).convert()
		self.fonte = Font("recursos/sprites/fonte.ttf", 8)

		self.botoes = [["LUTAR", "BOLSA"], ["NISSIMON", "FUGIR"]]
		self.estado = "botoes"
		self.botoesFuncoes = [[self.lutar, 0], [0, lambda: self.correr(cenaManager)]]
		self.botaoIndex = [0, 0]
		self.index = image.load("recursos/sprites/batalha/index.png").convert()
		self.hpBar = image.load("recursos/sprites/batalha/hp_bar.png").convert()
		self.botoesFundo = image.load("recursos/sprites/caixa_de_texto.png").convert()
		self.nissimonUi1 = image.load("recursos/sprites/batalha/nissimon_ui.png").convert()
		self.nissimonUi2 = flip(self.nissimonUi1, True, False)
		self.nissimon1 = cenaManager.party[0]
		self.nissimon2 = Nissimon(cenaManager.nissimonData["charmander"])
		self.sprite1 = image.load("recursos/sprites/nissimons/costas.png").convert()
		self.sprite2 = image.load("recursos/sprites/nissimons/frente.png").convert()
		#self.estado = "botao"
		self.ui1X = 164
		self.ui2X = 4
		self.ui1Y = 58
		self.ui2Y = 8
		
	
	def voltar(self):
		self.estado = "botoes"
		
	def lutar(self):
		self.estado = "ataques"
		
	def correr(self, cenaManager):
		cenaManager.fade(lambda: cenaManager.setJogo(ESTADOS.OVERWORLD))
		
	def setUp(self, cenaManager):
		self.botaoIndex = [0, 0]
		self.nissimon2 = Nissimon(cenaManager.nissimonData["charmander"])
		self.estado = "botoes"
		self.setUpBotoes(cenaManager)
		
	def setUpBotoes(self, cenaManager):
		cenaManager.botoes["cima"].setFuncao(lambda: self.setIndex(0, -1), False)
		cenaManager.botoes["baixo"].setFuncao(lambda: self.setIndex(0, 1), False)
		cenaManager.botoes["esquerda"].setFuncao(lambda: self.setIndex(-1, 0), False)
		cenaManager.botoes["direita"].setFuncao(lambda: self.setIndex(1, 0), False)
		cenaManager.botoes["b"].setFuncao(self.voltar, False)
		cenaManager.botoes["a"].setFuncao(self.fazerFuncao, False)
	
	def fazerFuncao(self):
		if self.estado=="botoes":
			if self.botoesFuncoes[self.botaoIndex[1]][self.botaoIndex[0]]:
				self.botoesFuncoes[self.botaoIndex[1]][self.botaoIndex[0]]()
		else:
			ataque = self.nissimon1.ataques[self.botaoIndex[1]][self.botaoIndex[0]]
			if ataque:
				self.nissimon2.hp -= self.calcularDano(self.cenaManager.movimentosData[ataque])
				self.nissimon2.hp = max(self.nissimon2.hp, 0)
				if self.nissimon2.hp==0:
					self.correr(self.cenaManager)
					
	def calcularDano(self, ataque):
		nssm1 = self.nissimon1
		nssm2 = self.nissimon2
		a = nssm1.stats[1] if ataque["categoria"]=="fisico" else nssm1.stats[4]
		d = nssm2.stats[2] if ataque["categoria"]=="fisico" else nssm2.stats[5]
		item = 1
		critico = 1
		temporal = 1
		insignia = 1
		stab = 1.5 if ataque["tipo"] in nssm1.tipos else 1
		tipo = 1
		rand = random.randint(217, 255)/255
		form1 = (2*nssm1.level/5+2)*ataque["poder"]*(a/d)
		return int(((form1/50)*item*critico+2)*temporal*insignia*stab*tipo*rand)
		
	def setIndex(self, x, y):
		self.botaoIndex[0] = max(min(self.botaoIndex[0]+x, 1), 0)
		self.botaoIndex[1] = max(min(self.botaoIndex[1]+y, 1), 0)

	def update(self, cenaManager):
		pass
	
	def show(self):
		self.display.fill((255, 255, 255))

		self.display.blit(self.sprite1, (16, 46))
		#draw.rect(self.display, (100, 200, 200), (184, 0, 56, 56))
		self.display.blit(self.sprite2, (192, 0))
		self.showUi()
	
	def showUi(self):
		self.display.blit(self.botoesFundo, (0, 102))
		self.showNissimonUi1()
		self.showNissimonUi2()
		
		botoes = self.botoes if self.estado=="botoes" else self.nissimon1.ataques
		textos = []
		for y in range(2):
			textos.append([])
			for x in range(2):
				if botoes[y][x]:
					textos[-1].append(self.fonte.render(botoes[y][x], 0, (0, 0, 0), (255, 255, 255)))
				else:
					textos[-1].append(self.fonte.render("-", 0, (0, 0, 0), (255, 255, 255)))
		textos1Largura = max(textos[0][0].get_width(), textos[1][0].get_width())
		textos2Largura = max(textos[0][1].get_width(), textos[1][1].get_width())
		xComeco = 128-(textos1Largura+textos2Largura)/2
		
		#draw.rect(self.display, (0, 0, 0), (xComeco-8, 109-3, textos1Largura+textos1Largura, 32), 1)
		for y in range(2):
			for x in range(2):
				offset = -1 if x==0 else 1
				if x==self.botaoIndex[0] and y==self.botaoIndex[1]:
					self.display.blit(self.index, (xComeco+3*offset-6+(textos1Largura+offset)*x, 109+16*y+2))
				
				self.display.blit(textos[y][x], (xComeco+3*offset+(textos1Largura+offset)*x, 109+16*y))
#		if self.estado=="botoes":
#			for y in range(2):
#				for x in range(2):
#									
#					texto = self.fonte.render(self.botoes[y][x], 0, (0, 0, 0), (255, 255, 255))
#					self.display.blit(texto, (72+x*xOffset, 108+y*16))
#		else:
#			xOffset = 72
#			for y in range(2):
#				for x in range(2):
#					if x==self.botaoIndex[0] and y==self.botaoIndex[1]:
#						self.display.blit(self.index, (64+x*xOffset, 108+y*16))

		

	def showNissimonUi1(self):
		self.display.blit(self.nissimonUi1, (self.ui1X, self.ui1Y))
		self.display.blit(self.fonte.render(self.nissimon1.nome, 0, (0, 0, 0), (255, 255, 255)), (self.ui1X+4, self.ui1Y+2))
		self.display.blit(self.hpBar, (self.ui1X+6, self.ui1Y+12))
		draw.rect(self.display, (95, 205, 8), (self.ui1X+18, self.ui1Y+14, int(self.nissimon1.hp/self.nissimon1.stats[0]*60), 3))
		
		level = self.fonte.render(f"lv{self.nissimon1.level}", 0, (0, 0, 0), (255, 255, 255))
		hp = self.fonte.render(f"{self.nissimon1.hp}/{self.nissimon1.stats[0]}", 0, (0, 0, 0), (255, 255, 255))
		levelX = (self.ui1X+83)-level.get_width()#self.ui1X+52
		self.display.blit(hp, (levelX-hp.get_width()-3, self.ui1Y+20))
		self.display.blit(level, (levelX, self.ui1Y+20))
		largura = int(self.nissimon1.xp/self.nissimon1.stats[0]*77)
		draw.rect(self.display, (82, 74, 255), (self.ui1X+82-largura, self.ui1Y+29, largura, 1))
	
	def showNissimonUi2(self):
		self.display.blit(self.nissimonUi2, (self.ui2X, self.ui2Y))
		self.display.blit(self.fonte.render(self.nissimon2.nome, 0, (0, 0, 0), (255, 255, 255)), (self.ui2X+8, self.ui2Y+2))
		self.display.blit(self.hpBar, (self.ui2X+10, self.ui2Y+12))
		draw.rect(self.display, (98, 205, 8), (self.ui2X+22, self.ui2Y+14, int(self.nissimon2.hp/self.nissimon2.stats[0]*60), 3))
		self.display.blit(self.fonte.render(f"lv{self.nissimon2.level}", 0, (0, 0, 0), (255, 255, 255)), (self.ui2X+8, self.ui2Y+20))

class ESTADOS(Enum):
	OVERWORLD = 0
	LUTA = 1
	estados = [OVERWORLD, LUTA]#, MENUPRINCIPAL
	estadosClasses = [Overworld, Luta]#MenuPrincipal, MenuConfiguracoes]
	
def telaParaDisplay(x, y):
	return [int(x/TELA_TAMANHO[0]*DISPLAY_TAMANHO_REAL[0]),
				int(y/TELA_TAMANHO[1]*DISPLAY_TAMANHO_REAL[1])]