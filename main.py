from pygame.font import (init, SysFont)
from pygame.time import Clock
from pygame.display import (set_mode, update)
from pygame.locals import (DOUBLEBUF, FULLSCREEN)
from scripts.cenas import CenaManager
from profilehooks import profile

init()

#@profile(filename="profile.prof")
def main():
	frame = 0
	fps = 30
	flags = DOUBLEBUF|FULLSCREEN
	tela = set_mode((1920, 1080), flags, 16)
	fonte = SysFont("Calibri", 16)
	cenaManager = CenaManager()

	clock = Clock()
	while cenaManager.rodando:
		cenaManager.update()
		cenaManager.show(tela)
		jogo = cenaManager.estados[cenaManager.estado]		
		#tela.blit(fonte.render(str(round(clock.get_fps())), 0, (100, 255, 255), (0, 0, 0)), (40, 40))
		m = ""
		for key in jogo.mapaManager.mapas:
			if jogo.mapaManager.mapas[key]:
				m += f"{key}:{jogo.mapaManager.mapas[key].filename} "
			else:
				m += f"{key}:0 "
		a = ""
		for key in jogo.mapaManager.mapas:
			if jogo.mapaManager.mapas[key]:
				a += f"{key}:{jogo.mapaManager.mapas[key].conexao} "
			else:
				a += f"{key}:0 "
#		tela.blit(fonte.render(str(m), 0, (100, 255, 255), (0, 0, 0)), (40, 60))
#		tela.blit(fonte.render(str(a), 0, (100, 255, 255), (0, 0, 0)), (40, 80))
#		tela.blit(fonte.render(f"{jogo.camera.x}|{jogo.camera.y}", 0, (100, 255, 255), (0, 0, 0)), (40, 80))
		update()
		clock.tick(fps)

main()