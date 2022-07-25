from __future__ import division
from pygame import (image, Surface, Rect, draw)
from pygame.locals import RLEACCEL
from time import time
from scripts.config import *
from tmx import TileMap

class MapaManager:
	def __init__(self, camera):
		self.fundo = None
		self.camera = camera
		self.display = Surface((DISPLAY_TAMANHO[0]+16, DISPLAY_TAMANHO[1]+16)).convert()
		self.mapa = None
		self.colisoes = None
		self.a = not False
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
		self.offsetX = 0
		self.offsetY = 0
		self.novoMapa("mapaTestes")
		self.updateDisplay(camera)
	
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
	
	
	def novoMapa(self, filename, warp=None):
		self.display.fill((0, 0, 0))
		del self.fundo
		del self.mapa
		del self.tileset
		del self.funcoes
		del self.grid
		del self.colisoes
		del self.animacoes
		del self.tiles
		
		self.animacoes = []
		self.camera.x = 0
		self.camera.y = 0
		self.offsetX = 0
		self.offsetY = 0
		print("name", filename)
		self.mapa = TileMap.load(f'recursos/mapas/{filename}.tmx')
		self.conseguirFundo(filename)
		if self.mapa.width<self.camera.largura:
			self.offsetX = (self.camera.largura-self.mapa.width)//2*16
		if self.mapa.height<self.camera.altura:
			self.offsetY = (self.camera.altura-self.mapa.height)//2*16
			
		self.funcoes = self.mapa.layers[-1].objects

		print("funcoes", self.funcoes)
		self.tileset = self.mapa.tilesets[0]
		
		print("tileset", self.tileset.name, "size", (self.tileset.tilewidth, self.tileset.tileheight))
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
		
	def emWarp(self, entidadeRect):
		for funcao in self.funcoes:
			if funcao.type=="warp":
				rect = Rect((funcao.x, funcao.y, funcao.width, funcao.height))
				if entidadeRect.colliderect(rect):
					return funcao
		return False
				
	def entrarWarp(self, Rect, jogo):
		for funcao in self.funcoes:
			if funcao.type=="warp" and self.emWarp(Rect):
				f = lambda: self.novoMapa(self.conseguirMapaWarp(funcao))
				jogo.fade(f)
				#self.novoMapa(self.conseguirMapaWarp(funcao))
				#jogo.fadein()
	
	def conseguirMapaWarp(self, warp):
		for propriedade in warp.properties:
			if propriedade.name=="mapa":
				return propriedade.value
	
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
			
	def conseguirRect(self, pos):
		x = pos[0]*self.tileset.tilewidth
		y = pos[1]*self.tileset.tileheight
		return Rect((x, y, self.tileset.tilewidth, self.tileset.tileheight))	
	
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
				self.display.blit(tiles[grid[0][y][x]], (x*tileset.tilewidth-(camera.x//16*16), y*tileset.tileheight-(camera.y//16*16)))
		self.display.set_colorkey(FUNDO_SPRITESHEET)

	
	def show(self, display):
		xDiff = self.camera.x%16
		yDiff = self.camera.y%16

		display.blit(self.fundo[0], (-self.camera.x%self.fundo[1][0]-self.fundo[1][0], -self.camera.y%self.fundo[1][1]-self.fundo[1][1]))
		display.blit(self.display, (-xDiff, -yDiff))