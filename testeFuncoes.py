import pygame as pg
from tmx import TileMap

pg.init()

tela = pg.display.set_mode((1920, 1080))

display = pg.Surface((256, 128)).convert()


while True:
	display.fill((0, 0, 0))
	tela.blit(pg.transform.scale(display, tela.get_size()), (0, 0))
	pg.display.update()