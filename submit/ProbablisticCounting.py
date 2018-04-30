import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
from decimal import Decimal
from fileRead import filereader

global BIT_MAP_SIZE
BIT_MAP_SIZE = 2000
global bit_map
bit_map = [0]*BIT_MAP_SIZE


def findHashcode(s):
	h = 0
	for c in s:
		h = (31 * h + ord(c)) & 0xFFFFFFFF
	return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000


def countZerosInBitMap():
		numOfZeros = 0
		for i in range(0, BIT_MAP_SIZE):
			if bit_map[i] == 0:
				numOfZeros += 1
		return numOfZeros


def ProbabCount():
	global bit_map
	flowMap = filereader(1)
	scatter_points = dict()

	with open('pcOut.txt', 'w') as outFile:
		for flow in flowMap.keys():
			tempFlow = flowMap[flow]
			actualCardinality = len(tempFlow)
			for destn in tempFlow:
				bitMap_ind = (findHashcode(flow + destn) & 0x7fffffff) % BIT_MAP_SIZE
				bit_map[bitMap_ind] = 1

			num_zeros = Decimal(countZerosInBitMap())
			Vn = num_zeros / Decimal(BIT_MAP_SIZE)

			estimatedCardinality = int((-1 * BIT_MAP_SIZE * math.log(Vn)))

			scatter_points[actualCardinality] = estimatedCardinality
			bit_map = [0] * BIT_MAP_SIZE

			outFile.write(str(flow) + "\t\t" + str(actualCardinality) + "\t\t" + str(estimatedCardinality) + "\n")
	outFile.close()

	fig = plt.figure()
	gx = scatter_points.keys()
	gy = scatter_points.values()
	plt.scatter(gx, gy, linewidths="1")
	# plt.plot(scatter_points.keys(), scatter_points.values(), marker="o", linewidth=".5")
	plt.title("Probablistic Counting")
	plt.xlabel("Estimate")
	plt.ylabel("Actual")
	fig.savefig('Probablistic.png', dpi=fig.dpi, bbox_inches='tight')
	plt.show()


ProbabCount()
