# Descripcion

import re

class Fraccion:

	def __init__ (self, *arg):

		if arg[0] == 0:
			self.__signo = 1
			self.__vector = [0,1,1]
			self.__valornumerico = 0.0
		elif len(arg) == 2:
			numerador, denominador = arg[0], arg[1]
			self.__valornumerico = numerador/denominador
			self.__signo = int(self.__valornumerico / abs(self.__valornumerico))
			self.__vector = [abs(numerador), abs(denominador), self.__signo]
		elif len(arg) == 1:
			self.__valornumerico = arg[0]
			if not isinstance(self.__valornumerico, int) and not isinstance(self.__valornumerico, float):
				raise TypeError(f'Entrada inválida, debe ser int o float. Es {type(self.__valornumerico)}')
			elif isinstance(self.__valornumerico, int):
				self.__signo = int(self.__valornumerico / abs(self.__valornumerico))
				self.__vector = [abs(self.__valornumerico), 1, self.__signo]
			else:
				self.__signo = int(self.__valornumerico / abs(self.__valornumerico))
				self.__vector = Fraccion.__DecimalFinito(abs(self.__valornumerico)) + [self.__signo]

		self.__Simplificar()

	def __repr__(self):
		numerador, denominador, signo = self.__vector

		if numerador == 0:
			return "0"
		elif denominador == 1:
			return f'{signo*numerador}'
		else:
			return f'{signo*numerador}:{denominador}'


	def __Simplificar(self):

		if self.__vector[0] == 0:
			self.__vector = [0,1,1]
			return

		a = self.__vector[0]
		b = self.__vector[1]
		Algunos, todos = Fraccion.__Factorizacion_prima(a, b)

		MCD = 1

		for primo in todos:
			MCD *= primo

		self.__vector[0] = a // MCD
		self.__vector[1] = b // MCD


	def getNumerador(self):
		return self.__vector[2]*self.__vector[0]

	def getDenominador(self):
		return self.__vector[1]

	def getValorNumerico(self):
		return self.__valornumerico


	def __add__(self, other):
		if not isinstance(other, Fraccion):
			other = Fraccion.__Clase(other)

		algunos, todos = Fraccion.__Factorizacion_prima(self.__vector[1], other.__vector[1])
		mcm = 1

		for i in algunos:
			mcm *= i

		a = self.__signo*self.__vector[0]*(mcm//self.__vector[1])
		b = other.__signo*other.__vector[0]*(mcm//other.__vector[1])

		nuevo_denominador = a + b

		return Fraccion.__Clase(nuevo_denominador, mcm)

	def __neg__(self):
		return Fraccion.__Clase(-self.__signo*self.__vector[0], self.__vector[1])

	def __sub__(self, other):
		return Fraccion.__Resta(self, other)

	def __mul__(self, other):
		if not isinstance(other, Fraccion):
			other = Fraccion.__Clase(other)

		salida = []
		for i in range(3):
			salida.append(self.__vector[i]*other.__vector[i])

		salida = [salida[2]*salida[0], salida[1]]

		return Fraccion.__Clase(*salida)

	def __truediv__(self, other):
		if not isinstance(other, Fraccion):
			other = Fraccion.__Clase(other)

		return Fraccion.__Division(self, other)

	def __rtruediv__(self, other):
		if not isinstance(other, Fraccion):
			other = Fraccion.__Clase(other)

		return Fraccion.__Division(other, self)

	def __pow__(self, other):
		a = self.__vector[0]
		b = self.__vector[1]

		if not isinstance(other, Fraccion):
			other = Fraccion(other)

		if other.__vector[0] % 2 != 0 and self.__vector[2] == -1:
			signo = -1
		else:
			signo = 1

		a = (a**other.__vector[0])**(1/other.__vector[1])
		b = (b**other.__vector[0])**(1/other.__vector[1])

		if other.__vector[2] == -1:
			a, b = b, a

		if int(a) - a != 0 or int(a) - a != 0:
			return Fraccion.__Clase(signo*a/b)
		else:
			a, b = int(a), int(b)

		return Fraccion.__Clase_3arg(a,b,signo)

	def invertir(self):
		return 1 / self


	@classmethod
	def __Clase(cls, *arg):
		return cls(*arg)

	@classmethod
	def __Clase_3arg(cls, *arg):
		a = arg[0]*arg[2]
		b = arg[1]
		return cls(a,b)

	@staticmethod
	def __Resta(a, b):
		return a + (-b)

	@staticmethod
	def __Division(a, b):
		return a * b**-1

	@classmethod
	def Decimal_infinito_periodico(cls, Numero):
		if isinstance(Numero, int):
			return cls(abs(Numero), 1, Numero // abs(Numero))

		Parte_entera = int(Numero)
		if Parte_entera != 0:
			signo = Parte_entera // abs(Parte_entera)
			Parte_entera = abs(Parte_entera)
		else:
			signo = 1
		str_numero = str(Numero).split(".")

		if int(str_numero[1]) == 0:
			return cls(Parte_entera, 1, signo)

		patron, grupo0 = Fraccion.__SubStr_repetida(str_numero[1])
		if patron == "":
			patron = str_numero[1]
	#		return cls(*Fraccion.__DecimalFinito(Numero))

		str_decimal = re.sub(grupo0 + "$", "", str_numero[1])
		if str_decimal == "":
			str_decimal = "0"

		fraccion_entero = cls(signo*Parte_entera)
		fraccion_decimal1 = cls(signo*int(str_decimal), 10**(len(str_decimal)))
		denominador_ = "9"*len(patron)
		fraccion_decimal2 = cls(signo*int(patron), int(denominador_)*10**(len(str_decimal)))

		return fraccion_entero + fraccion_decimal1 + fraccion_decimal2


	@staticmethod
	def __DecimalFinito(Numero):
		Parte_entera = int(Numero)
		str_numero = str(Numero)

		str_decimal = str(str_numero).replace(f'{str(Parte_entera)}.', "")
		orden = len(str_decimal)

		return [Parte_entera*10**orden + int(str_decimal), 10**orden]


	@staticmethod
	def __Factorizacion_prima(*arg):

		Lista = [*arg]
		for i in range(len(Lista)):
			if Lista[i] == 0:
				Lista.pop(i)
			elif Lista[i] < 0:
				raise TypeError("Entrada negativa. Solo ingresa números enteros positivos.")

		if len(Lista) == 0:
			raise TypeError("Entrada inválida. Ingresa uno o más números enteros positivos diferentes a 0.")

		try:
			entrada = open("TOOLS/Estos_son_primos.txt", "r")
		except FileNotFoundError:
			print("Archivo con primos no se encontró.")
			return
		primos = entrada.readlines()
		entrada.close()

		divide_alguno = []
		divide_todos = []
		div_numeros = Divisivilidad(*Lista)

		for primo in primos:
			primo = int(primo.strip())
			divisibles = (True,)

			if Divisivilidad.AllOnes(div_numeros):
				break

			while any(divisibles):

				divisibles = div_numeros % primo

				if any(divisibles):
					divide_alguno.append(primo)
				else:
					continue

				if all(divisibles):
					divide_todos.append(primo)

				div_numeros.Dividir(primo)



		return tuple(divide_alguno), tuple(divide_todos)

	@staticmethod
	def __SubStr_repetida(cadena):
		search_ = re.search(r'(\d+)\1{2,}\Z', cadena)
		try:
			return search_.group(1), search_.group(0)
		except AttributeError:
			return "", ""


class Divisivilidad:

	def __init__(self, *arg):
		self.tupla = arg

	def __mod__(self, n):
		if not isinstance(n, int):
			raise TypeError(f'El divisor es un {type(n)}. Debe ser int')

		salida = []
		for numero in self.tupla:
			if numero % n == 0:
				salida.append(True)
			else:
				salida.append(False)

		return tuple(salida)

	def Dividir(self, other):
		if not isinstance(other, int):
			raise TypeError(f'El divisor es un {type(other)}. Debe ser int')

		salida = []

		for i in range(len(self.tupla)):
			if self.tupla[i] % other == 0:
				salida.append(self.tupla[i]//other)
			else:
				salida.append(self.tupla[i])

		self.tupla = tuple(salida)

	@staticmethod
	def AllOnes(objeto):
		aux = []
		for numero in objeto.tupla:
			aux.append(numero == 1)

		return all(aux)


	@classmethod
	def __Clase(cls,tupla):
		return cls(*tupla)
