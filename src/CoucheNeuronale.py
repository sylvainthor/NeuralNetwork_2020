#!/usr/bin/env python
import Neurone
import Biais
import MatriceLiaisons


class CoucheNeuronale:
	"""
	Classe représentant une couche de neurone, cachés ou pas
	"""
	def __init__(self, nbNeurones, hasBiais=False, biaisForce=1):
		if type(nbNeurones) is not int:
			raise TypeError('Bad type')
		if type(hasBiais) is not bool:
			raise TypeError('Bad bool')
		if type(biaisForce) is not int:
			raise TypeError('Bad type')

		self.mesNeurones = []
		self.nbNeurones = nbNeurones
		self.hasBiais = hasBiais
		for i in range(0, self.nbNeurones):
			self.mesNeurones.append(Neurone.Neurone())
		if hasBiais:
			self.mesNeurones.append(Biais.Biais(biaisForce))

	def calculer_valeur_neurones(self, matrice, valeur_neurones):
		"""
		Calcul la valeur des neurones de cette couche en additionnant la valeur
		des neurones de la couche précédente fois le poid correspondant
		@param matrice: la matrice des poids
		@param valeur_neurones: la valeur des neurones de la couche précédante
		"""
		if type(valeur_neurones) is not list or type(matrice) is not MatriceLiaisons.MatriceLiaisons :
			raise TypeError('Bad type')
		for x in valeur_neurones:
			if type(x) is not float and type(x) is not int:
				raise TypeError('Bad type')
		m = matrice.get_matrice()
		for i in range(0, self.nbNeurones):
			self.mesNeurones[i].calcul_valeur(m[i], valeur_neurones)

	def set_valeur(self, valeurs):
		if type(valeurs) is not list:
			raise TypeError('Bad type')
		for x in valeurs:
			if type(x) is not int and type(x) is not float:
				raise TypeError('Bad type')
		if len(valeurs) != self.nbNeurones:
			raise ValueError('lenght of tab incorrect')

		i = 0
		for x in valeurs:
			self.mesNeurones[i].set_valeur(x)
			i += 1

	def get_valeur(self):
		tab = []
		for i in range(0, self.nbNeurones):
			tab.append(self.mesNeurones[i].get_valeur())
		return tab

	def get_nb_neurones(self):
		return self.nbNeurones

	def get_nb_element(self):
		"""
		A la différence de get_nb_neurones, renvoie le nombre d'element
		donc en comptant le biais
		@return: nombre d'elements
		"""
		if self.hasBiais:
			return self.nbNeurones+1
		else:
			return self.nbNeurones

	def get_neurones(self):
		"""
		renvoie les neurones et seulement les neurones
		@return:
		"""
		if self.hasBiais:
			tab = self.mesNeurones[:]
			tab.pop()
			return tab
		else:
			return self.mesNeurones

	def get_element(self):
		return self.mesNeurones


# test :
def main():
	cn = CoucheNeuronale(5)


if __name__ == '__main__':
	main()