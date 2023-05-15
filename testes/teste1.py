import inspect
from teste2 import funcao

func = inspect.getsourcelines(funcao)[0][1:]
i = 0
while i<len(func):
	l = func[i].strip()
	if l[0:3]=="if ":
		while " "
	else:
		parentesesFinal = len(l)-l[::-1].index(')')-1
		l = l[:parentesesFinal] + ", end=' '" + l[parentesesFinal:]
		eval(l)
#for i in range(len(func)):
#	parentesesFinal = len(func[i])-func[i][::-1].index(')')-1
#	func[i] = func[i][:parentesesFinal] + ", end=' '" + func[i][parentesesFinal:]
#for l in func:
#	eval(l)