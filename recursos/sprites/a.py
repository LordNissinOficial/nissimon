import pygame as pg

pg.init()

tela = pg.display.set_mode((1920, 100))
display = pg.Surface((256, 144))
img = pg.Surface((16, 16))
for y in range(16):
	for x in range(16):
		if (y+x)%4==0:
			img.set_at((x, y), (255, 100, 100))
		else:
			img.set_at((x, y), (100, 100, 100))
i = 0
while True:
	for y in range(9):
		for x in range(16):
			display.blit(img, (x*16, y*16))
			break
		break
	i += 1
	if i==20:
		img.scroll(0, 1)
		i = 0
	
	pg.transform.scale(display, tela.get_size(), tela)
	pg.display.update()