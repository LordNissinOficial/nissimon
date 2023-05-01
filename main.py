from pygame.font import (init, SysFont)
from pygame.time import Clock
from pygame.display import (set_mode, update)
from pygame.locals import (DOUBLEBUF, FULLSCREEN)
from scripts.cenas import CenaManager
from profilehooks import profile

init()

@profile(filename="profile.prof")
def main():
	frame = 0
	fps = 30
	flags = DOUBLEBUF|FULLSCREEN
	tela = set_mode((1920, 1080), flags, 16)
	fonte = SysFont("Calibri", 14)
	cenaManager = CenaManager()
	tela.fill((203, 203, 203))
	clock = Clock()
	while cenaManager.rodando:
		cenaManager.update()
		cenaManager.show(tela)
		jogo = cenaManager.estados[cenaManager.estado]		
		tela.blit(fonte.render(str(round(clock.get_fps())), 0, (100, 255, 255), (0, 0, 0)), (40, 40))
		#tela.blit(fonte.render("pode mover:"+str(jogo.podeMover), 0, (100, 255, 255), (0, 0, 0)), (40, 50))
#		tela.blit(fonte.render("evento andar:"+str(jogo.jogador.emEventoAndar), 0, (100, 255, 255), (0, 0, 0)), (40, 65))
		update()
		clock.tick(fps)

main()