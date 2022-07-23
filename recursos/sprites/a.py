import pygame as pg

pg.init()

tela = pg.display.set_mode((1920, 100))
display = pg.Surface((256, 144))
img = pg.image.load("jogador.png").convert()#pg.Surface((16, 16))

def scrollX(screenSurf, offsetX):
	width, height = screenSurf.get_size()
	copySurf = screenSurf.copy()
	screenSurf.blit(copySurf, (offsetX, 0))
	if offsetX < 0:
		screenSurf.blit(copySurf, (width + offsetX, 0), (0, 0, -offsetX, height))
	else:
		screenSurf.blit(copySurf, (0, 0), (width - offsetX, 0, offsetX, height))
		
def scrollY(screenSurf, offsetY):
	width, height = screenSurf.get_size()
	copySurf = screenSurf.copy()
	screenSurf.blit(copySurf, (0, offsetY))
	if offsetY < 0:
		screenSurf.blit(copySurf, (0, height+offsetY), (0, 0, width, -offsetY))
	else:
		screenSurf.blit(copySurf, (0, 0), (0, height-offsetY, width, offsetY))
			
def scroll(img, offset):
	imgCopy = 
	scrollX(img, offset[0])
	scrollY(img, offset[1])
	
#for y in range(16):
#	for x in range(16):
#		if (y+x)%4==0:
#			img.set_at((x, y), (255, 100, 100))
#		else:
#			img.set_at((x, y), (100, 100, 100))
i = 0
while True:
	display.fill((0, 0, 0))
	for y in range(9):
		for x in range(16):
			display.blit(img, (x*16, y*16))
			#break
#		break
	i += 1
	if i%10==0:
		scroll(img, (1, 0))
#		i = 0
	
	pg.transform.scale(display, tela.get_size(), tela)
	pg.display.update()