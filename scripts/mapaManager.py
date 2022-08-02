from __future__ import division
from pygame import (image, Surface, Rect, draw)
from pygame.locals import RLEACCEL
from time import time
from copy import copy
from json import load as loadJson
from scripts.config import *
from tmx import TileMap

class MapaManager:
	def __init__(self, camera):
		self.camera = camera
		self.display = Surface((DISPLAY_TAMANHO[0]+16, DISPLAY_TAMANHO[1]+16)).convert()
		self.mapas = {"centro": 0, "cima": 0, "baixo": 0, "esquerda": 0, "direita": 0}
		self.mapasSalvos = {}
		self.conexoes = loadJson(open("recursos/data/conexoes.json", "r"))
		self.novoMapa("casaTestes")
		#self.updateDisplay(camera)
	
#	def __getstate__(self):
#		state = self.__dict__.copy()
#		#state["tilesetImg"] = image.tostring(state['tilesetImg'], "RGB")
#	#	print(state['tiles'], end="\n"*4)
#		print(self.tiles)
#		for key, tile in list(state["tiles"].items()):
#			#print(key, state['tiles'][key])
#			state['tiles'][key] = image.tostring(tile, "RGB")
#			
#		#print(state['tiles'])
#		return state
#	
#	def __setstate__(self, state):
#		state["tilesetImg"] = image.fromstring(state['tilesetImg'], [128, 128], "RGB")
#		state["tilesetImg"].set_colorkey((0, 0, 0))
#		for key, tile in state["tiles"].items():
#			#print(key, state["tiles"][key])
#			state["tiles"][key] = image.fromstring(tile, [16, 16], "RGB")
#		#print(state["tiles"])
#		self.__dict__.update(state)	
	
	
	def novoMapa(self, filename, warp=False):
		print("\n", filename, "\n")
		self.display.fill((0, 0, 0))
		for mapa in self.mapas:	
			if not self.mapas[mapa]: continue
			if filename==self.mapas[mapa].filename:
				self.mapas[mapa].conexao = "centro"
				self.mapas["centro"] = copy(self.mapas[mapa])
				break
				
		for conexao in self.conexoes[filename]:
			conseguiuMapa = False
			for mapa in self.mapas:
					if not self.mapas[mapa]: continue
					if self.conexoes[filename][conexao][0]==self.mapas[mapa].filename:
						self.mapas[mapa].conexao = conexao
						conseguiuMapa = True
						self.mapas[conexao] = copy(self.mapas[mapa])
						break

			if not conseguiuMapa:
				if self.conexoes[filename][conexao][0] in self.mapasSalvos:
					self.mapas[conexao] = copy(self.mapasSalvos[self.conexoes[filename][conexao][0]])
				else:
					self.mapas[conexao] = Mapa(self.conexoes[filename][conexao][0], self.camera, self.conexoes[filename][conexao][1], conexao)
					self.mapasSalvos[self.mapas[conexao].filename] = copy(self.mapas[conexao])
		
		
		for conexao2 in ["cima", "baixo", "esquerda", "direita"]:
			if not conexao2 in self.conexoes[filename]:
				self.mapas[conexao2] = 0
		if not self.mapas["centro"] or warp:
			self.mapas["centro"] = Mapa(filename, self.camera, 0, "centro")
		self.updateDisplay(self.camera)
	
	def emWarp(self, entidadeRect):
		for funcao in self.mapas["centro"].funcoes:
			if funcao.type=="warp":
				rect = Rect((funcao.x, funcao.y, funcao.width, funcao.height))
				if entidadeRect.colliderect(rect):
					return funcao
		return False
				
	def entrarWarp(self, Rect, jogo):
		for funcao in self.mapas["centro"].funcoes:
			if funcao.type=="warp" and self.emWarp(Rect):
				f = lambda: self.novoMapa(self.conseguirMapaWarp(funcao), True)
				jogo.fade(f)
	
	def conseguirMapaWarp(self, warp):
		for propriedade in warp.properties:
			if propriedade.name=="mapa":
				return propriedade.value

	def podeMover(self, x, y, eJogador):
			if eJogador:
				if 0<=x<len(self.mapas["centro"].colisoes[0]) and 0<=y<len(self.mapas["centro"].colisoes) and self.mapas["centro"].colisoes[y][x]==65:
					return [True, "centro"]
				else:
					if y<0 and self.mapas["cima"] and self.mapas["cima"].colisoes[-1][x+self.mapas["cima"].offset]==65:
						self.novoMapa(self.mapas["cima"].filename)
						return [True, "cima"]
						
					elif y==len(self.mapas["centro"].colisoes) and self.mapas["baixo"] and self.mapas["baixo"].colisoes[0][x+self.mapas["baixo"].offset]==65:
						self.novoMapa(self.mapas["baixo"].filename)
						return [True, "baixo"]
					
					elif x<0 and self.mapas["esquerda"] and self.mapas["esquerda"].colisoes[y+self.mapas["esquerda"].offset][-1]==65:
						self.novoMapa(self.mapas["esquerda"].filename)
						return [True, "esquerda"]
					elif x==len(self.mapas["centro"].colisoes[0]) and self.mapas["direita"] and self.mapas["direita"].colisoes[y+self.mapas["direita"].offset][0]==65:
						print("novo", self.mapas["direita"].filename)
						self.novoMapa(self.mapas["direita"].filename)
						return [True, "direita"]
					else:
						print(x, y, self.mapas["centro"].filename)
						
	def updateAnimacoes(self, camera):
		for mapa in self.mapas:
			if not self.mapas[mapa]: continue
			self.mapas[mapa].updateAnimacoes(camera)
				
	def updateDisplay(self, camera):
		self.display.fill((0, 0, 0))
		for key in self.mapas:
			if not self.mapas[key]: continue
			self.mapas[key].updateDisplay(camera)
		
	def show(self, display):
		for key in self.mapas:
			if not self.mapas[key]:
				continue
			self.mapas[key].show(display)

class Mapa:
	def __init__(self, filename, camera, offset, conexao, warp=None):
		self.filename = filename
		self.fundo = None
		self.camera = camera
		self.display = Surface((DISPLAY_TAMANHO[0]+16, DISPLAY_TAMANHO[1]+16)).convert()
		self.mapa = None
		self.colisoes = None
		self.grid = None
		self.tileset = None
		self.animacoes  = None
		self.tilesDic = None
		self.funcoes = None
		self.tiles = None
		self.minYAntigo = None
		self.maxYAntigo = None
		self.minXAntigo = None
		self.maxXAntigo = None
		self.conexao = conexao
		self.offset = offset
		self.offsetX = 0
		self.offsetY = 0
		self.load(warp)
		#self.updateDisplay(camera)
	
#	def __getstate__(self):
#		state = self.__dict__.copy()
#		#state["tilesetImg"] = image.tostring(state['tilesetImg'], "RGB")
#	#	print(state['tiles'], end="\n"*4)
#		print(self.tiles)
#		for key, tile in list(state["tiles"].items()):
#			#print(key, state['tiles'][key])
#			state['tiles'][key] = image.tostring(tile, "RGB")
#			
#		#print(state['tiles'])
#		return state
#	
#	def __setstate__(self, state):
#		state["tilesetImg"] = image.fromstring(state['tilesetImg'], [128, 128], "RGB")
#		state["tilesetImg"].set_colorkey((0, 0, 0))
#		for key, tile in state["tiles"].items():
#			#print(key, state["tiles"][key])
#			state["tiles"][key] = image.fromstring(tile, [16, 16], "RGB")
#		#print(state["tiles"])
#		self.__dict__.update(state)	
	
	
	def load(self, warp=None):
		self.display.fill((0, 0, 0))
		self.animacoes = []

		self.offsetX = 0
		self.offsetY = 0
		print("novo mapa", self.filename)
		self.mapa = TileMap.load(f'recursos/mapas/{self.filename}.tmx')
		self.conseguirFundo(self.filename)
		if self.mapa.width<self.camera.largura:
			self.offsetX = (self.camera.largura-self.mapa.width)//2*16
		if self.mapa.height<self.camera.altura:
			self.offsetY = (self.camera.altura-self.mapa.height)//2*16
			
		self.funcoes = self.mapa.layers[-1].objects
		
		self.tileset = self.mapa.tilesets[0]
		
		self.tilesPraDicionario(self.tileset.tiles)
		tilesetImg = image.load(f"recursos/sprites/tilesets/{self.tileset.image.source.split('/')[-1]}").convert()
		self.grid = []
		self.colisoes = []
		self.tiles = self.tilesetPraLista(tilesetImg, self.tileset.tilewidth, self.tileset.tileheight)
		self.animacoes = self.conseguirAnimacoes(self.tileset)
		del tilesetImg
		self.carregarMapa()
		self.updateDisplay(self.camera)
	
	def conseguirAnimacoes(self, tileset):
		animacoes = []
		for tile in tileset.tiles:
			for frame in tile.animation:
				frame.tileid += 1
			animacoes.append([tile.animation, 0, time()])
			print(tile.animation[0].duration)
		return animacoes
		
	def conseguirFundo(self, filename):
		try:
			img = image.load("recursos/sprites/fundos/"+filename+".png")
		except:
			img = Surface((16, 16)).convert()
			img.fill((57, 57, 57))
		self.fundo = [Surface((DISPLAY_TAMANHO[0]+img.get_width(), DISPLAY_TAMANHO[1]+img.get_height())).convert(), img.get_size()]

		for y in range(DISPLAY_TAMANHO[1]//img.get_height()+2):
			for x in range(DISPLAY_TAMANHO[0]//img.get_width()+2):
				self.fundo[0].blit(img, (x*img.get_width(), y*img.get_height()))

	def tilesPraDicionario(self, tiles):
		del self.tilesDic
		self.tilesDic = {}
		for tile in tiles:
			self.tilesDic[tile.id+1] = {}
			for propriedade in tile.properties:
				valor = propriedade.value
				valor = valor!="true"
				self.tilesDic[tile.id+1][propriedade.name] = valor
	
	def carregarMapa(self):
		y = 0
		for layer in self.mapa.layers:
			if layer.name!="funcoes":
				self.layerPraGrid(layer)
			
	def tilesetPraLista(self, tileset, tileLargura, tileAltura):
		lista = {}
		for y in range(tileset.get_height()//tileAltura):
			for x in range(tileset.get_width()//tileLargura):
				surface = Surface((tileLargura, tileAltura))
				rect = Rect((x*tileLargura, y*tileAltura, tileLargura, tileAltura))
				surface.blit(tileset, (0, 0), rect)
				if not self.transparente(surface):
					surface = surface.convert()
					surface.set_colorkey(None, RLEACCEL)
					lista[y*int(tileset.get_width()/tileLargura)+x+1] = surface
		return lista
		
##retorna true se a surface for toda transparente
	def transparente(self, surface):
		return surface.get_bounding_rect(1).width<1

	def layerPraGrid(self, layer):
		tiles = layer.tiles
		grid = []
		gridAppend = grid.append
		l = []
		lAppend = l.append
		y, x = 0, 0
		for tile in tiles:
			lAppend(tile.gid)
			x += 1
			if x==self.mapa.width:
				x = 0
				y += 1
				gridAppend(l)
				l = []
				lAppend = l.append
		if layer.name!="colisoes":
			self.grid.append(grid)
		else:
			self.colisoes = grid

	def updateAnimacoes(self, camera):
		for animacao in self.animacoes:
			idAntigo = animacao[1]
			tileIdAntigo = animacao[0][idAntigo].tileid
			if time()-animacao[2]>=animacao[0][animacao[1]].duration/1000:
				animacao[2] = time()
				animacao[1]+=1
				if animacao[1]==len(animacao[0]):
					animacao[1] = 0
			if animacao[1]!=idAntigo:
				copia = self.tiles[animacao[0][0].tileid].copy()
				self.tiles[animacao[0][0].tileid] = self.tiles[animacao[0][animacao[1]].tileid].copy()
				self.tiles[animacao[0][animacao[1]].tileid] = copia
				self.updateDisplay(camera)
				
	def updateDisplay(self, camera):
		self.display.fill(FUNDO_SPRITESHEET)
		if self.conexao=="cima":
			self.minY = max(int((camera.y+self.mapa.height*16)/16), 0)
			self.maxY = min(self.minY+camera.altura+1, self.mapa.height)
			self.minX = max(int(camera.x/16), 0)
			self.maxX = min(self.minX+camera.largura+1, self.mapa.width)
		elif self.conexao=="baixo":
			self.minY = max(int((camera.y-self.mapa.height*16)/16), 0)
			self.maxY = min(self.minY+camera.altura+1, self.mapa.height)
			self.minX = max(int(camera.x/16), 0)
			self.maxX = min(self.minX+camera.largura+1, self.mapa.width)
		elif self.conexao=="esquerda":
			self.minY = max(int(camera.y/16), 0)
			self.maxY = min(self.minY+camera.altura+1, self.mapa.height)
			self.minX = max(int((camera.x+self.mapa.width*16)/16), 0)
			self.maxX = min(self.minX+camera.largura+1, self.mapa.width)
		elif self.conexao=="direita":
			self.minY = max(int(camera.y/16), 0)
			self.maxY = min(self.minY+camera.altura+1, self.mapa.height)
			self.minX = max(int((camera.x-self.mapa.width*16)/16), 0)
			self.maxX = min(self.minX+camera.largura+1, self.mapa.width)
		elif self.conexao=="centro":
			self.minY = max(int(camera.y/16), 0)
			self.maxY = min(self.minY+camera.altura+1, self.mapa.height)
			self.minX = max(int(camera.x/16), 0)
			self.maxX = min(self.minX+camera.largura+1, self.mapa.width)
		
		if self.mapa.width<camera.largura:
			self.minX = 0
			self.maxX = self.mapa.width
		if self.mapa.height<camera.altura:
			self.minY = 0
			self.maxY = self.mapa.height

		self.minYAntigo = self.minY
		self.maxYAntigo = self.maxY
		self.minXAntigo = self.minX
		self.maxXAntigo = self.maxX

		tiles = self.tiles
		tileset = self.tileset
		grid = self.grid
		
		for y in range(self.minY, self.maxY):
			for x in range(self.minX, self.maxX):
				offsetX = 0
				offsetY = 0
				if self.conexao=="cima":
					offsetY = -self.mapa.height*16
				elif self.conexao=="baixo":
					offsetY = self.mapa.height*16
				elif self.conexao=="esquerda":
					offsetX = -self.mapa.width*16
				elif self.conexao=="direita":
					offsetX = self.mapa.width*16

				self.display.blit(tiles[grid[0][y][x]], (x*tileset.tilewidth-(camera.x//16*16)+offsetX, y*tileset.tileheight-(camera.y//16*16)+offsetY))
		self.display.set_colorkey(FUNDO_SPRITESHEET)
	
	def show(self, display):
		xDiff = self.camera.x%16
		yDiff = self.camera.y%16
		if self.conexao=="centro":
			display.blit(self.fundo[0], (-self.camera.x%self.fundo[1][0]-self.fundo[1][0], -self.camera.y%self.fundo[1][1]-self.fundo[1][1]))

		display.blit(self.display, (-xDiff, -yDiff))
		