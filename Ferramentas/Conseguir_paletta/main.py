#conseguir todas as cores das imagens e paletas shiny
import os
from PIL import Image
#dir = os.get_dir()
#print(dir)
pokemons = list(os.walk("./pokemon"))
#print(len(pokemons))
coresPokemon = []
for i in range(1, len(pokemons)):
#	print(pokemons[i][0], pokemons[i][-1])
#	print(pokemons[i][0][2::]+pokemons[i][-1][0])
	for imgName in pokemons[i][-1]:
		if ".png" in imgName:
		
			img = Image.open(pokemons[i][0][2::]+"/"+pokemons[i][-1][0])
			cores = [key for key in img.palette.colors.keys()]
			print(pokemons[i][0].split("/")[2], *cores)
			for cor in cores:
				if not cor in coresPokemon:
					coresPokemon.append(cor)
#	if i>100:
#		break

print(len(coresPokemon))