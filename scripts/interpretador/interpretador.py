
class Interpretador:
	def __init__(self):
		pass
	
	def interpretar(self, codigo):
		flags = {}
		orgs = {}
		index = 0
		codigoSplit = codigo.split("\n")
		print("-"*12+"CODIGO"+"-"*12, "\n")
		print("\n".join(codigoSplit), "\n"*2, "-"*12+"OUTPUT"+"-"*12, "\n")
		for i, linha in enumerate(codigoSplit):
			if len(linha)==0:
				continue
			if linha[0]=="@":
				orgs[linha] = i
		while index<len(codigoSplit):
			linha = codigoSplit[index].split(" ")
#			if not linha:
#				continue
			#print(linha)
			if len(linha)==0:
				index+=1
				continue
			if linha[0]=="msg":
				print(" ".join(linha[1::]))
			elif linha[0]=="var":
				flags[linha[1]]=linha[2]
				#print(flags[linha[1]])
			elif linha[0]=="if_jump":
				#print(2)
				if linha[1]=="True":
					index = orgs[linha[2]]
				elif flags[linha[1]]=="True":
					index = orgs[linha[2]]
			elif linha[0]=="jump":
				index = orgs[linha[1]]
			elif linha[0]=="END": break
			index += 1
					
interpretador = Interpretador()
codigo = """
var a False
if_jump a @a
jump @b
@a
msg iae como vc esta!
END
@b
msg estou bem.
END"""
interpretador.interpretar(codigo)