# Descripcion

from TOOLS.fraccion import *


def main():

	Numero = 1/6
	Numero2 = 8
	numero3 = 0

	print(f'El constructor tendrá como argumento {Numero}')

	frac = Fraccion.Decimal_infinito_periodico(Numero)
	frac2 = Fraccion(Numero2, 3)
	frac3 = Fraccion(numero3)

	print(f'La representación del objeto quedó: {frac}')
	print(f'{frac} / {frac2} = {frac / frac2}')

	print(frac.invertir())

	print(frac**frac2)





def SubStr_repetida(cadena):
	largo = len(cadena)
	maximo = largo//2 + 1

	coinci = []
	control = []

	for m in range(largo):
		n_maximo = maximo + m
		if n_maximo > largo:
			n_maximo = largo + 1
		for n in range(m+1, n_maximo):
			substr = cadena[m:n]

			if substr in control:
				continue
			control.append(substr)

			largo_sub = len(substr)
			recurrencia = cadena.count(substr)
			if recurrencia == 1 or recurrencia == 0:
				continue

			r = list(range(2, recurrencia + 1))
			for i in reversed(r):
				print(substr, substr*i, cadena[-largo_sub*i:], cadena[-largo_sub*i:] == substr*i)

				if cadena[-largo_sub*i:] == substr*i:
					coinci.append(substr)

	print(coinci)

def SubStr_repetida2(cadena):
	largo = len(cadena)
	maximo = largo//2 + 1
	len_patron = 1

	coinci = dict()
	subcadenas = []

	for m in range(1,largo):
		largo2 = len(cadena[-m:])

		if largo2 % len_patron != 0:
			continue

		print(f'm = {m}')
		subcadenas.append(cadena[-m:])
		print(subcadenas)
		print("-----------------------------------------------------------------------------in")
		for substr in [subcadenas.copy()[-1]]:
			largo_sub = len(substr)
			indice = largo2 // largo_sub

			print("\t",1, indice+1, substr, cadena[-m:])

			for r in range(1,indice+1):
				print("\t\t", substr, substr*indice, cadena[-m:], substr*indice == cadena[-m:], len_patron)

				if substr*indice == cadena[-m:]:
					coinci[substr] = indice
					len_patron += largo_sub
				else:
					subcadenas.remove(substr)
					break
#					pass

		print("-----------------------------------------------------------------------------out")
	print(coinci)
	print(subcadenas)


def SubStr_repetida3(cadena):
	largo = len(cadena)
	maximo = largo//2 + 1
	len_patron = 1
	Mas_repite = 1
	salida = "Nada"

	subcadenas = dict()

	for m in range(1,largo):
		substr = cadena[-m:]
		subcadenas[substr] = 0

		if m >= maximo+1:
			break

		for n in range(m, largo, m):
			check = cadena[-n:]
			factor = n//m
			if substr*factor == check:
				subcadenas[substr] += 1
			else:
				break

	for sub in subcadenas:
		if subcadenas[sub] > Mas_repite:
			Mas_repite = subcadenas[sub]
			salida = sub

	return salida, Mas_repite

main()
