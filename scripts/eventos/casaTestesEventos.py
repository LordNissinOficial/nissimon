import time
def eventoTeste(jogo, lista):
	lista.append(lambda: jogo.travarPersonagens(emEvento=True))
	lista.append(lambda: jogo.cenaManager.botoes["start"].travarBotao(evento=True))
	
	lista.append(lambda: jogo.moverJogador(-1, 0, emEvento=True))
	lista.append(lambda: jogo.mapaManager.mapas["centro"].npcs[0].mover(1, 0, jogo, evento=True))
	lista.append(lambda: jogo.mapaManager.mapas["centro"].npcs[0].mover(1, 0, jogo, evento=True))
	lista.append(lambda: jogo.mapaManager.mapas["centro"].npcs[0].mover(-1, 0, jogo, evento=True))
	lista.append(lambda: jogo.mapaManager.mapas["centro"].npcs[0].mover(-1, 0, jogo, evento=True))
	lista.append(lambda: jogo.mapaManager.mapas["centro"].npcs[0].olhar(0, 1, jogo, evento=True))
	lista.append(lambda: jogo.dialogoManager.comecarDialogo(["teste de dialogo com evento.", "alo? alo?", "isso deu certo?"], evento=True))
	
	lista.append(lambda: jogo.destravarPersonagens(emEvento=True))
	lista.append(lambda: jogo.cenaManager.botoes["start"].destravarBotao(evento=True))
	#lista.append(lambda: jogo.a(emEvento=True))
	#lista.append(lambda: jogo.moverJogador(0, 1, emEvento=True))
	#jogo.moverJogador(-1, 0)
	#print("deu certo:D")