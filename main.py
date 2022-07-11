from pygame import Rect
from pygame.font import (init, SysFont)
from pygame.time import Clock
from pygame.display import (set_mode, flip, update)
from pygame.locals import (DOUBLEBUF, FULLSCREEN)
#import pygame as pg
from scripts.cenas import CenaManager
from profilehooks import profile

#pg.init()
init()

#@profile(filename="profile.prof")
def main():
	frame = 0
	flags = DOUBLEBUF|FULLSCREEN
	tela = set_mode((1920, 1080), flags, 16)
	fonte = SysFont("Calibri", 10)
	cenaManager = CenaManager()
	clock = Clock()
	while cenaManager.rodando: #and frame<60:
		#frame += 1
		cenaManager.update()
		cenaManager.show(tela)
		tela.blit(fonte.render(str(round(clock.get_fps())), 0, (100, 255, 255), (0, 0, 0)), (40, 40))
#		jogador = cenaManager.estados[cenaManager.estado].jogador
#		tela.blit(fonte.render(f"{jogador.movendo}", 0, (100, 255, 255), (62, 39, 49)), (40, 50))
		#tela.blit(fonte.render(str(cenaManager.spriteManager.load.cache_info()), 0, (100, 255, 255), (62, 39, 49)), (40, 50))
		update()
		cenaManager.deltaTime = clock.tick(40)/1000

main()