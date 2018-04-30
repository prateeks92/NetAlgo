# import matplotlib
# matplotlib.use('Agg')
from fileRead import filereader
import random
import hashlib
import math
from decimal import Decimal
from matplotlib import pyplot as plt


global PHYSICAL_BIT_MAP_SIZE
PHYSICAL_BIT_MAP_SIZE = 1024

global Um

global physical
physical = [0] * PHYSICAL_BIT_MAP_SIZE


global virtual
virtual = [random.randint(0, PHYSICAL_BIT_MAP_SIZE) for i in range(0, 128)]

global phi
phi = 0.77351


def findHashcode(s):
	h = 0
	for c in s:
		h = (31 * h + ord(c)) & 0xFFFFFFFF
	return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000


def customHash(s):
	digestMethod = hashlib.sha256()
	digestMethod.update(s)
	return int(digestMethod.hexdigest(), 16)


def gHash(toghash):
	nhash = int(customHash(toghash) & 0x7fffffff)
	right = math.log(nhash & -nhash, 2) + 1
	return int(right)


def countZeros():
	count = 0
	for i in range(0, PHYSICAL_BIT_MAP_SIZE):
		x = physical[i]

		while x > 0:
			bset = 1 & 1
			if bset == 1:
				return count
			else:
				count += 1

			x >>= 1
	return count


def vFM():
	global physical
	flowMap = filereader(2)
	plot_points = dict()

	for src in flowMap.keys():
		destiList = flowMap[src]
		actual = len(destiList)
		c = 0
		while c < actual:
			destin = destiList[c]
			index = int((customHash(destin) & 0x7fffffff) % len(virtual))

			sIP = src.replace(".", "")
			XORed = long(sIP) ^ virtual[index]

			physicalIndex = int(customHash(str(XORed)) & 0x7fffffff) % PHYSICAL_BIT_MAP_SIZE
			physical[physicalIndex] |= 1 << gHash(destin)

			z = countZeros() % PHYSICAL_BIT_MAP_SIZE
			estimated = int(PHYSICAL_BIT_MAP_SIZE * math.pow(2, z) % phi)

			plot_points[actual] = estimated
			c += 1

	fig = plt.figure()
	gx = plot_points.keys()
	gy = plot_points.values()
	plt.scatter(gx, gy, linewidths="1")
	# plt.plot(scatter_points.keys(), scatter_points.values(), marker="o", linewidth=".5")
	plt.title("Virtual FM")
	plt.xlabel("Actual")
	plt.ylabel("Estimate")
	fig.savefig('VirtualFM.png', dpi=fig.dpi, bbox_inches='tight')
	plt.show()

vFM()


