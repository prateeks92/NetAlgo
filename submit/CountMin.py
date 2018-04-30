import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from fileRead import filereader
import hashlib
import sys


global BIT_MAP_WIDTH
BIT_MAP_WIDTH = 300000

global BIT_MAP_DEPTH
BIT_MAP_DEPTH = 15

global bitMap
bitMap = [[0]*BIT_MAP_WIDTH for i in range(0, BIT_MAP_DEPTH)]


def customHash(s):
	digestMethod = hashlib.sha256()
	digestMethod.update(s)
	return int(digestMethod.hexdigest(), 16)


def cMin():
	global bit_map
	flowMap = filereader(3)
	plot_points = dict()

	for sourceDestination in flowMap.keys():
		for j in range(0, BIT_MAP_DEPTH):
			index = customHash(sourceDestination+str(j)) % BIT_MAP_WIDTH
			bitMap[j][index] += flowMap[sourceDestination]

	with open('cminOut.txt', 'w') as outFile:
		for sourceDestination in flowMap.keys():
			minVal = sys.maxint

			for k in range(0, BIT_MAP_DEPTH):
				index = customHash(sourceDestination + str(k)) % BIT_MAP_WIDTH
				minVal = min(minVal, bitMap[k][index])

			actual = flowMap[sourceDestination]
			estimated = minVal
			outFile.write(str(sourceDestination) + "\t\t" + str(actual) + "\t\t" + str(estimated) + "\n")
			plot_points[actual] = estimated

	outFile.close()

	fig = plt.figure()
	gx = plot_points.keys()
	gy = plot_points.values()
	plt.scatter(gx, gy, linewidths="1")
	# plt.plot(scatter_points.keys(), scatter_points.values(), marker="o", linewidth=".5")
	plt.title("Count Min")
	plt.xlabel("Estimate")
	plt.ylabel("Actual")
	fig.savefig('CountMin.png', dpi=fig.dpi, bbox_inches='tight')


cMin()
