import time
def eventoTeste(jogo, lista):
	lista.append(lambda: jogo.moverJogador(-1, 0, emEvento=True))
	#lista.append("espere 1")
	lista.append(lambda: jogo.moverJogador(-1, 0, emEvento=True))
	lista.append(lambda: jogo.moverJogador(0, -1, emEvento=True))
	lista.append(lambda: jogo.moverJogador(0, -1, emEvento=True))
	lista.append(lambda: jogo.a(emEvento=True))
	#lista.append(lambda: jogo.moverJogador(0, 1, emEvento=True))
	#jogo.moverJogador(-1, 0)
	#print("deu certo:D")