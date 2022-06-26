import pygame as pg
import pickle, copy
from mapaManager import MapaManager
from jogador import Jogador
from config import *


pg.init()

class Jogo():
	def __init__(self, jogoId):
		self.display = pg.Surface(DISPLAY_TAMANHO)
		self.mapaManager = MapaManager()
		self.cor = (75, 53, 97)
		self.jogoId = jogoId
#		self.jogadores = {}
		self.jogadores[55].pos.x = 22*16
		self.updates = 0
	
	def updateJogador(self, jogadorId):
		self.jogadores[jogadorId].update(self)
#		jogador = self.jogadores[jogadorId]
#		jogador.camera.moverPara(jogador.pos.x, jogador.pos.y)
		
	def update(self): pass
		#self.jogadores[0].pos.x += 2
		#self.camera.pos.x += 1
		#self.camera.moverPara(self.jogadores[0].pos.x, self.jogadores[0].pos.y)
		#print("camera", self.camera.pos.x)
#		raise Exception("a")


	def show(self, jogadorId):
		if self.updates==0:
			self.update()
			
		self.updates += 1
		if self.updates==len(self.jogadores):
			self.updates = 0
			
		
		self.updateJogador(jogadorId)
		
		
		self.showDisplay(jogadorId)
		data = pickle.dumps(pg.image.tostring(self.display, "RGB"))
		self.jogadores[jogadorId].s.send(data)
		self.jogadores[jogadorId].s.send(pickle.dumps(PACKET_FIM))

##mostra no display o jogo especifico pro cliente
	def showDisplay(self, jogadorId):
		jogador = self.jogadores[jogadorId]
		self.display.fill(self.cor)
		#self.jogadores[0].img.set_colorkey((0, 0, 0))
		self.mapaManager.show(jogador.camera, self.display, self.jogadores)
		jogador.showUi(self.display)
#		for outroJogador in self.jogadores.values():
#			outroJogador.show(self.display, jogador.camera)
		#pg.draw.rect(self.display, (244, 244, 255), (4, DISPLAY_TAMANHO[1]-20, 16, 16))
		#display.blit(self.jogadores[0].img, (128-8, 64-8))
	
	def lidarEventos(self, jogadorId, eventos):
		jogador = self.jogadores[jogadorId]
		#print(eventos)
		for evento in eventos:
			
			if evento["tipo"] in [pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION]:
				pos = list(evento["data"]["pos"])
				pos[0] = int(pos[0]/TELA_TAMANHO[0]*DISPLAY_TAMANHO[0])
				pos[1] = int(pos[1]/TELA_TAMANHO[1]*DISPLAY_TAMANHO[1])
				jogador.botaoCima.pressionandoMouse(pos)
				jogador.botaoBaixo.pressionandoMouse(pos)
				jogador.botaoDireita.pressionandoMouse(pos)
				jogador.botaoEsquerda.pressionandoMouse(pos)
				
			elif evento["tipo"]==pg.MOUSEBUTTONUP:
				pos = list(evento["data"]["pos"])
				pos[0] = int(pos[0]/TELA_TAMANHO[0]*DISPLAY_TAMANHO[0])
				pos[1] = int(pos[1]/TELA_TAMANHO[1]*DISPLAY_TAMANHO[1])
				jogador.botaoCima.tirandoMouse(pos)
				jogador.botaoBaixo.tirandoMouse(pos)
				jogador.botaoDireita.tirandoMouse(pos)
				jogador.botaoEsquerda.tirandoMouse(pos)