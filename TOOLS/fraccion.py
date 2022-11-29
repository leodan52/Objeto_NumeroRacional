# Descripcion



class Fraccion:

	def __init__ (self, *arg):

		if arg[0] == 0:
			self.signo = 1
			self.vector = [0,1,1]
		elif len(arg) == 2:
			numerador, denominador = arg[0], arg[1]
			self.valornumerico = numerador/denominador
			self.signo = int(self.valornumerico / abs(self.valornumerico))
			self.vector = [abs(numerador), abs(denominador), self.signo]
		elif len(arg) == 1:
			self.valornumerico = arg[0]
			if not isinstance(self.valornumerico, int) and not isinstance(self.valornumerico, float):
				raise TypeError(f'Entrada inválida, debe ser int o float. Es {type(self.valornumerico)}')
			elif isinstance(self.valornumerico, int):
				self.signo = int(self.valornumerico / abs(self.valornumerico))
				self.vector = [abs(self.valornumerico), 1, self.signo]
			else:
				self.signo = int(self.valornumerico / abs(self.valornumerico))
				self.vector = Fraccion.Decimal2Fraccion(abs(self.valornumerico)) + [self.signo]

		self.Simplificar()

	def __repr__(self):
		numerador, denominador, signo = self.vector

		if numerador == 0:
			return "0"
		elif denominador == 1:
			return f'{signo*numerador}'
		else:
			return f'{signo*numerador}:{denominador}'


	def Simplificar(self):

		if self.vector[0] == 0:
			self.vector = [0,1,1]
			return

		a = self.vector[0]
		b = self.vector[1]
		Algunos, todos = Fraccion.Factorizacion_prima(a, b)

		MCD = 1

		for primo in todos:
			MCD *= primo

		self.vector[0] = a // MCD
		self.vector[1] = b // MCD


	def getNumerador(self):
		return self.vector[0]

	def getDenominador(self):
		return self.vector[1]

	def getSigno(self):
		return self.vector[2]


	def __add__(self, other):
		if not isinstance(other, Fraccion):
			other = Fraccion.Clase(other)

		algunos, todos = Fraccion.Factorizacion_prima(self.vector[1], other.vector[1])
		mcm = 1

		for i in algunos:
			mcm *= i

		a = self.signo*self.vector[0]*(mcm//self.vector[1])
		b = other.signo*other.vector[0]*(mcm//other.vector[1])

		nuevo_denominador = a + b

		return Fraccion.Clase(nuevo_denominador, mcm)

	def __neg__(self):
		return Fraccion.Clase(-self.signo*self.vector[0], self.vector[1])

	def __sub__(self, other):
		return Fraccion.Resta(self, other)

	def __mul__(self, other):
		if not isinstance(other, Fraccion):
			other = Fraccion.Clase(other)

		salida = []
		for i in range(3):
			salida.append(self.vector[i]*other.vector[i])

		salida = [salida[2]*salida[0], salida[1]]

		return Fraccion.Clase(*salida)

	def __truediv__(self, other):
		if not isinstance(other, Fraccion):
			other = Fraccion.Clase(other)

		return Fraccion.Division(self, other)

	def __pow__(self, other):
		a = self.vector[0]
		b = self.vector[1]

		if not isinstance(other, Fraccion):
			other = Fraccion(other)

		if other.vector[0] % 2 != 0 and self.vector[2] == -1:
			signo = -1
		else:
			signo = 1


		a = (a**other.vector[0])**(1/other.vector[1])
		b = (b**other.vector[0])**(1/other.vector[1])

		if other.vector[2] == -1:
			a, b = b, a

		if int(a) - a != 0 or int(a) - a != 0:
			return Fraccion.Clase(signo*a/b)
		else:
			a, b = int(a), int(b)

		return Fraccion.Clase_3arg(a,b,signo)


	@classmethod
	def Clase(cls, *arg):
		return cls(*arg)

	@classmethod
	def Clase_3arg(cls, *arg):
		a = arg[0]*arg[2]
		b = arg[1]
		return cls(a,b)

	@staticmethod
	def Resta(a, b):
		return a + (-b)

	@staticmethod
	def Division(a, b):
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

		patron, veces = Fraccion.SubStr_repetida(str_numero[1])
		if veces == 1:
			patron = str_numero[1]
	#		return cls(*Fraccion.Decimal2Fraccion(Numero))

		longitud_repetida = len(patron*veces)
		aux = list(str_numero[1])
		del aux[-longitud_repetida:]
		str_decimal = "".join(aux)
		longitud_decimal = len(str_decimal)
		if str_decimal == "":
			str_decimal = "0"

		fraccion_entero = cls(signo*Parte_entera)
		fraccion_decimal1 = cls(signo*int(str_decimal), 10**(len(str_decimal)))
		denominador_ = "9"*len(patron)
		fraccion_decimal2 = cls(signo*int(patron), int(denominador_)*10**longitud_decimal )

		return fraccion_entero + fraccion_decimal1 + fraccion_decimal2


	@staticmethod
	def Decimal2Fraccion(Numero):
		Parte_entera = int(Numero)
		str_numero = str(Numero)

		str_decimal = str(str_numero).replace(f'{str(Parte_entera)}.', "")
		orden = len(str_decimal)

		return [Parte_entera*10**orden + int(str_decimal), 10**orden]


	@staticmethod
	def Factorizacion_prima(*arg):

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
	def SubStr_repetida(cadena):
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

			for n in range(m, largo+1, m):
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
	def Clase(cls,tupla):
		return cls(*tupla)
