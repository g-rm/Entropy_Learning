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



def bootstrap(rat_shuffled_samples, reyes_window_size=20):

	"""
	Apllies change point analysis and group values above
	standart deviation of a given shuffled/permuted samples of n-rats.

	Parameters:
	-----------
	rat_shuffled_samples : array-like
		list of n-samples of shuffled/permuted data of one rat
		ex.	[[s1],[s2], ...[sn]]

	full_window_size : int, optional, default: 20
        Size of the total walking window (sum of two halfs)

	Returns:
	--------
	cp_odds : array-like
		Group of change-point odds value
	"""

	arr = rat_shuffled_samples

	cp_odds = []
	n_samples = len(arr)

	for i in range(n_samples):
		#Applies change point in all shuffled datas
		aux = arr[i]
		aux = reyes_cp(aux, reyes_window_size)
		aux = aux.dropna().values

		#Group max change point value of each sample
		cp_odds.append(aux.max())

	#Turns list to array
	cp_odds = np.asarray(cp_odds)

	return cp_odds


def real_cp(cp_odds, dt=.1, p=.95):
	"""
	Determines limiar for wich the change point will be real,
	or valid.

	Parameters
	----------
	cp_odds : array-like
		Array with change-points values of one rat

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

	#log prevents issues between short dt and high ranges
	arr = np.log(cp_odds)
	density_edges = [None] * 2

	area_sum = np.zeros(1)
	real_cp = np.zeros(1)

	#Some aliases
	min = arr.min()
	max = arr.max()
	range_diff = max - min

	density_edges = generate_pdf(arr, (min, max), dt)

	#More aliases
	density = density_edges[0]
	bin_edges = density_edges[1]

	bins = int(range_diff/dt) + 1
	for j in range(bins):
		if area_sum <= p:
			#integrates area
			area_sum += density[j] * dt
			#greater bin edge
			real_cp = bin_edges[j+1]

	return	np.exp(real_cp), area_sum
