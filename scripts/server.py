import pygame as pg
import socket, threading
import pickle, sys
from jogador import Jogador
from jogo import Jogo

pg.init()
pg.display.set_mode((1, 1))
jogadorIdAtual = 0
jogos = {}

			
def lidarCliente(clienteSocket, addr, jogoId, jogadorId):
	#clienteSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	global jogos
	print(f"conectado com cliente [{addr[0]}] no jogo [{jogoId}].")
	clienteSocket.send(pickle.dumps([jogoId, jogadorId]))#manda o id e jogoid para o cliente
	while True:
		try:#se ocorrer um erro o cliente saiu da socket
			data = clienteSocket.recv(2048)
		except socket.error as e:
			print(e)
			break
		if not data:
			break
		msg = pickle.loads(data)
		#print(f"cliente [{addr[0]}]: {msg}")
		if msg=="SAIR":
			break
		if msg=="CONSEGUIR JOGO":##manda a tela do jogo para o cliente
			jogos[jogoId].show(jogadorId)
		############
		elif msg[0]=="LIDAR EVENTOS":##lida com os eventos do cliente
			jogos[jogoId].lidarEventos(jogadorId, msg[1])
			
	print(f"cliente [{addr[0]}] disconectou.")
	jogos[jogoId].jogadores.pop(jogadorId)#tira o jogador do jogo dele
	if len(jogos[jogoId].jogadores)==0:
		jogos.pop(jogoId)##se o jogo nao tiver jogadores ele é excluido
		print(f"fechando jogo [{jogoId}].")
	clienteSocket.close()
	

def conseguirIp():#consegue o ip da maquina rodando o server
	s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s1.connect(("8.8.8.8", 80))
	ip = s1.getsockname()[0]
	s1.close()
	return ip



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip   = conseguirIp()
porta = 8000

try: 
	s.bind((ip, porta))
	print(f"conectando servidor no ip [{ip}] e na porta [{porta}].")
except socket.error as msg:
	print("falha ao criar o servidor.\nmensagem de erro:")
	print(msg)
	sys.exit()
print("servidor conectado.")

s.listen(0)
print("escutando por coneções.")

while True:
	c, addr = s.accept()
	
	#cria ou adiciona o cliente para um jogo
	if len(jogos.keys())==0:
		jogos[jogadorIdAtual//2] = Jogo(jogadorIdAtual//2)
		print("criado jogo Novo com id [0].")
	elif len(jogos[list(jogos.keys())[-1]].jogadores)==2:
		jogos[jogadorIdAtual//2] = Jogo(jogadorIdAtual//2)
		print(f"criado jogo Novo com id [{jogadorIdAtual//2}].")
	
	clienteThread = threading.Thread(target=lidarCliente, args=(c, addr, jogadorIdAtual//2, jogadorIdAtual%2,))
	clienteThread.start()
	jogos[jogadorIdAtual//2].jogadores[jogadorIdAtual%2] = (Jogador(c, jogadorIdAtual%2))
	
	jogadorIdAtual += 1
s.close()