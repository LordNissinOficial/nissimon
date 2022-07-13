from pygame.font import (init, SysFont)
from pygame.time import Clock
from pygame.display import (set_mode, flip, update)
from pygame.locals import (DOUBLEBUF, FULLSCREEN)
from scripts.cenas import CenaManager
from profilehooks import profile

init()

#@profile(filename="profile.prof")
def main():
	frame = 0
	flags = DOUBLEBUF|FULLSCREEN
	tela = set_mode((1920, 1080), flags, 16)
	fonte = SysFont("Calibri", 10)
	cenaManager = CenaManager()

	clock = Clock()
	while cenaManager.rodando:
		cenaManager.update()
		cenaManager.show(tela)
		tela.blit(fonte.render(str(round(clock.get_fps())), 0, (100, 255, 255), (0, 0, 0)), (40, 40))
		update()
		cenaManager.deltaTime = clock.tick(30)/1000

main()