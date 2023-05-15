from scripts.eventos import *
from time import time
class EventoManager():
	def __init__(self, jogo):
		self.jogo = jogo
		self.lista = []
		self.terminouAcao = False
		self.comecouAcao = False
		self.timerInicial = 0
		self.timerDuracao = 0
		
	def update(self):
		#print("rodando o script")
		if self.lista:
			if self.timerInicial:
				if time()-self.timerInicial>=self.timerDuracao:
					self.timerInicial = 0
					self.timerDuracao = 0
					self.terminouAcao =True
			if not self.comecouAcao:
				print("comecou acao", self.lista[0])
				self.comecouAcao = True
				if type(self.lista[0])==str:
					if self.lista[0].split(" ")[0]=="espere":
						self.timerInicial = time()
						self.timerDuracao = float(self.lista[0].split(" ")[1])
						return
				self.lista[0]()				
	
			if self.terminouAcao:
				#print("terminou acao")
#				print()
				self.lista.pop(0)
				self.terminouAcao = False
				self.comecouAcao = False

	def rodarEventoScript(self, evento):
		if self.lista: return
		self.lista = []
		eval(f"{self.jogo.mapaManager.mapas['centro'].filename}Eventos.{evento}(self.jogo, self.lista)")
		#print(self.lista, 123)
		#self.rodarScript()
		#thread = Thread(target=self.rodarScript)
#		thread.run()

