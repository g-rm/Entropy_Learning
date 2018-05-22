import numpy as np
import pandas as pd
from functions.gallistel_information import reyes_cp
from functions.generate_pdf import generate_pdf

def shuffle_data(arr, n_times):

	"""
	Randomly shuffles data n_times

	Parameters:
	-----------
	arr : array or list
		list of arrays to be shuffled

	n_times : int
		How many times data will be shuffled

	Returns:
	--------
	shuffled : array_like
	"""

	shuffled = [[None] * n_times] * len(arr)
	for i in range(len(arr)):
		shuffled[i] = [np.random.permutation(arr[i]) for j in range(n_times)]

	return shuffled



def bootstrap(rats_shuffled_samples, std='False'):

	"""
	Apllies change point analysis and group values above
	standart deviation of a given shuffled/permuted samples of n-rats.

	Parameters:
	-----------
	rats_shuffled_samples : array-like
		list of m-samples of shuffled/permuted data of n rats
		(n < m).
		ex.	[[[m1],[m2]],[m3]] when len(n) equals n-rats equals 2

	std : array-like
		if True returns standart deviation of samples

	Returns:
	--------
	cp_odds : array-like
		Group of change-point odds values above the standart deviation

	std : array-like
		standart deviation of all m-samples of n-rats
	"""

	arr = rats_shuffled_samples

	n_rats = len(arr)
	cp_odds = [[] for i in range(n_rats)]
	std = [[] for i in range(n_rats)]		#

	for i in range(n_rats):
		n_samples = len(arr[i])
		for j in range(n_samples):

			#Applies change point in all shuffled datas
			aux = arr[i][j]
			aux = reyes_cp(aux, 20)

			#Gets only odds values above standart deviation
			aux = aux.dropna().values
			std[i].append(aux.std())		#
			arr[i][j] = aux[aux >= aux.std()]

			#Concatenates all change point odds of n samples in one array
			cp_odds[i].extend(arr[i][j])

		#Turns list to array
		cp_odds[i] = np.asarray(cp_odds[i])

	if std=='True':							#
		return cp_odds, std

	return cp_odds


def real_cp(cp_odds, dt, p=.95):
	"""
	Determines limiar for wich the change point will be real,
	or valid.

	Parameters
	----------
	cp_odds : array-like
		A list of n array with change-point data of n_rats

	dt : float
		Defines the number of equal-width bins in the given range

	p : float
		Confidence of the conclusions about change point value

	Returns:
	--------

	real_cp : float
		Infimum value for which the change point will be valid

	area_sum : float
	 	number between 0 and 1 that represents total integrated
		area
	"""

	arr = cp_odds
	n_rats = len(arr)

	density_edges = [None] * 2

	area_sum = [0] * n_rats
	real_cp = [0] * n_rats

	for i in range(n_rats):

		#Some aliases
		min = arr[i].min()
		max = arr[i].max()
		range_diff = max - min

		density_edges = generate_pdf(arr[i], (min, max), dt)

		#More aliases
		density = density_edges[0]
		bin_edges = density_edges[1]

		bins = int(range_diff/dt) + 1
		for j in range(bins):
			if area_sum[i] <= p:
				#integrates area
				area_sum[i] += density[j] * dt
				#greater bin edge
				real_cp[i] = bin_edges[j+1]

	return	real_cp, area_sum



def bootstrap_v2(arr):

	"""
	Creates a histogram and validates change point values

	Parameters:
	-----------
	arr : array-like
		array or list of n-samples of shuffled/permuted
		data to analysis

	Returns:
	--------
	density : array_like
	"""

	#Applies change point in all shuffled datas
	n_rats = len(arr)
	std = [[None] * len(arr[0])] * n_rats

	for i in range(n_rats):
		n_samples = len(arr[i])
		for j in range(n_samples):
			arr[i][j] = reyes_cp(arr[i][j], 20)
			aux = arr[i][j].dropna().values
			std[i][j] = aux.std()
			aux = aux[aux >= aux.std()]

	"""
	#Concatenates all change point odds of n samples in one array
	cp_odds = [None] * n_rats
	for i in range(len(arr)):
		n_samples = len(arr[i])
		cp_odds[i] = np.concatenate([arr[i][j] for j in range(n_samples)])
	"""

	return arr, std
