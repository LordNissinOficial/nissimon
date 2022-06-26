#import pygame as pg
from pygame.locals import (QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP)
from pygame.draw import line
from scripts.uiComponentes import Botao
from scripts.config import *
from pygame import event# as event
from pygame import Surface
#from pygame.transform import scale


class Inventario:
	def __init__(self, cenaManager):
		self.display = Surface(DISPLAY_TAMANHO_REAL).convert()
		self.displayMochila = Surface(DISPLAY_TAMANHO).convert()
		self.displayMochila.fill((115, 62, 57))
		self.spriteManager = cenaManager.spriteManager
		self.botoes = {}
		self.slots = [None for i in range(16)]
		self.slots[0] = "antidoto"
		#self.slots = [[None for x in range(10)] for y in range(9)]
		self.textoCor = (62, 39, 49)
		self.fundoCor = (115, 62, 57)
		self.setUpBotoes(cenaManager)
		
	def setUpBotoes(self, cenaManager):
		botoes = self.botoes
		
		botoes["inventario"] = Botao(208, 8, lambda: cenaManager.setJogo(0))
		botoes["inventario"].imgNormal = (8, 0, 2, 2)
		botoes["inventario"].imgPressionando = (8, 2, 2, 2)
		#self.aberto = True
#		self.slotIMG = 
#	
#	def toggle(self):
#		self{.aberto = not self.aberto
	
	def update(self, cenaManager):
		for botao in self.botoes:
			self.botoes[botao].update()
		self.lidarEventos(cenaManager)
		
	def show(self):
		#if not self.aberto:	return
		self.display.fill(COR_FUNDO)
		self.display.blit(self.displayMochila, (48, 0))
		self.display.blit(self.spriteManager.fonte.render("items chave", 0, self.textoCor, self.fundoCor), (128-self.spriteManager.fonte.size("items chave")[0]//2, 4))
		for index, slot in enumerate(self.slots[0:6]):
			
			if slot:
				self.display.blit(self.spriteManager.fonte.render(slot, 0, self.textoCor, self.fundoCor), (64, 38-13+16*index))
			line(self.display, self.textoCor, (64, 38+16*index), (190, 38+16*index))
#		img = self.spriteManager.load("spritesheets/ui", (14, 0, 2, 2))
#		for y in range(9):
#			for x in range(10):
#				self.display.blit(img, (48+x*16, y*16))
		
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
					
					
def telaParaDisplay(x, y):
	return [int(x/TELA_TAMANHO[0]*DISPLAY_TAMANHO_REAL[0]),
				int(y/TELA_TAMANHO[1]*DISPLAY_TAMANHO_REAL[1])]