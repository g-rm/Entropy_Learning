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



def bootstrap(rats_shuffled_samples):

	"""
	Apllies change point analysis and group values above
	standart deviation of a given shuffled/permuted samples of n-rats.

	Parameters:
	-----------
	rats_shuffled_samples : array-like
		list of m-samples of shuffled/permuted data of n rats
		(m > n).
		ex.	[[[m1],[m2]],[m3]] when len(n) equals n-rats equals 2

	Returns:
	--------
	cp_odds : array-like
		Group of change-point odds value
	"""

	arr = rats_shuffled_samples

	n_rats = len(arr)
	cp_odds = [[] for i in range(n_rats)]

	for i in range(n_rats):
		n_samples = len(arr[i])
		for j in range(n_samples):

			#Applies change point in all shuffled datas
			aux = arr[i][j]
			aux = reyes_cp(aux, 20)
			aux = aux.dropna().values

			#Group max change point values of each sample
			cp_odds[i].append(aux.max())

		#Turns list to array
		cp_odds[i] = np.asarray(cp_odds[i])

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
