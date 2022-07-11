import pygame as pg
import os, time

pg.init()
tela = pg.display.set_mode((1920, 1080))
display = pg.Surface((256, 128))
pokemons = list(os.walk("./pokemon"))
for i in range(len(pokemons)):
	for imgName in pokemons[i][-1]:
		display.fill((255, 255, 255))
		if ".png" in imgName and not "back" in imgName:
			#print(1)
			img = pg.image.load(pokemons[i][0][2::]+"/"+imgName)
			display.blit(img, (128-img.get_width()/2, 64-img.get_height()/2))
			pg.transform.scale(display, tela.get_size(), tela)
			pg.display.update()
			time.sleep(0.1)