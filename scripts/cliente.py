import pygame as pg
import socket, pickle
#from jogo import Jogo
#from jogador import Jogador
from config import *

pg.font.init()
def recvData():
	data = s.recv(4096)
	finalData = b""
	#print(data, end="\naa"*2)
	i = 0
	while data and i<51:
		#print(data, end="\n"*2)
		if PACKET_FIM in str(data):
			#print("fim")
			finalData += data[:str(data).find(PACKET_FIM)]
			#print(data, "\n")
			break
		finalData += data
		#finalData.append(data)
		data = s.recv(4096)
		i += 1
	#print(i)
	#print(data, "\n")
	#print(len(finalData))
	return pickle.loads(finalData)
	
s = socket.socket()
s.connect((IP, 8000))
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
data = s.recv(1024)
#print(data)
#print("id data", data, "\n"*4)
jogoId, jogadorId = pickle.loads(data)
#print("id", (jogoId, jogadorId), "\n"*4)
print("id", jogoId, "jogo id", jogadorId)

flags = pg.FULLSCREEN | pg.DOUBLEBUF
tela = pg.display.set_mode((1920, 1080), flags, 16)
#display = pg.Surface((12*16, 6*16)).convert()
clock = pg.time.Clock()

font = pg.font.SysFont("Calibri", 10)

def show():
	#print(1)
	#s.send(pickle.dumps("CONSEGUIR JOGO"))
	jogo = recvData()#s.recv(1024)
	#print(4)
	#print("show data ", data, "\n"*4)
	#jogo = pickle.loads(data)#pickle.loads(data)
	#print("jogo", jogo, "\n"*4)
	s.send(pickle.dumps("CONSEGUIR JOGO"))
	tela.blit(pg.transform.scale(pg.image.fromstring(jogo, DISPLAY_TAMANHO, "RGB"), tela.get_size()), (0, 0))
#	jogo.showDisplay(display)
#	tela.blit(pg.transform.scale(display, tela.get_size()), (0, 0))
#	pg.draw.
	tela.blit(font.render(str(round(clock.get_fps())), 0, (40, 40, 60)), (20, 20))
#	tela.blit(font.render(str(jogo.camera.pos), 0, (255, 255, 200)), (20, 40))
	pg.display.update()
	#del jogo
	
rodando = True

s.send(pickle.dumps("CONSEGUIR JOGO"))

pg.event.set_blocked(None)
pg.event.set_allowed([pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION])

while rodando:
		
	eventos = [{"tipo": evento.type, "data": evento.dict} for evento in pg.event.get()]
	if len(eventos)>0:
		s.send(pickle.dumps(["LIDAR EVENTOS", eventos]))
		
	show()	
	clock.tick(30)	