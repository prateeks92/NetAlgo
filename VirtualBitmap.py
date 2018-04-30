import matplotlib
matplotlib.use('Agg')
from fileRead import filereader
import random
import hashlib
import math
from decimal import Decimal
from matplotlib import pyplot as plt


global VIRTUAL_BIT_MAP_SIZE
VIRTUAL_BIT_MAP_SIZE = 2000

global PHYSICAL_BIT_MAP_SIZE
PHYSICAL_BIT_MAP_SIZE = 3000000

global Vm

global physical
physical = [0] * PHYSICAL_BIT_MAP_SIZE

global virtual
virtual = []
for i in range(0, VIRTUAL_BIT_MAP_SIZE):
	virtual.append(random.randint(0, PHYSICAL_BIT_MAP_SIZE))

global flowMap


def customHash(s):
	digestMethod = hashlib.sha256()
	digestMethod.update(s)
	return int(digestMethod.hexdigest(), 16)


def physicalBitMap():
	global VIRTUAL_BIT_MAP_SIZE
	global PHYSICAL_BIT_MAP_SIZE
	global physical
	global virtual
	global flowMap

	flowMap = filereader(2)

	sortedFlowKeys = sorted(flowMap.keys())
	for sourceIP in sortedFlowKeys:
		destinationList = flowMap[sourceIP]
		count = 0
		while count < len(destinationList):
			destination = destinationList[count]
			ind = int((customHash(destination) & 0x7fffffff) % VIRTUAL_BIT_MAP_SIZE)

			src = sourceIP.replace(".", "")
			xored = long(src) ^ virtual[ind]

			physicalInd = int((customHash(str(xored)) & 0x7fffffff) % PHYSICAL_BIT_MAP_SIZE)
			physical[physicalInd] = 1
			count += 1


def countNumberOfZeros():
	global physical
	c = 0
	for i in range(0, len(physical)):
		if physical[i] == 0:
			c += 1
	return c


def findCardinality(source, count):
	global Vm
	global flowMap
	Vm = countNumberOfZeros()

	scatter_points = dict()

	Um = Decimal(Vm) / Decimal(PHYSICAL_BIT_MAP_SIZE)
	Us = Decimal(count) / Decimal(VIRTUAL_BIT_MAP_SIZE)

	actualCardinality = len(flowMap[source])

	# s logVm - s log Vs
	estimatedCardinality = int(((VIRTUAL_BIT_MAP_SIZE * math.log(Um)) + (-1 * VIRTUAL_BIT_MAP_SIZE * math.log(Us))))

	return actualCardinality, estimatedCardinality


def estimateSpread():
	global flowMap
	global physical
	scatter_points = dict()

	for sourceIP in flowMap.keys():
		c = 0

		for i in range(0, VIRTUAL_BIT_MAP_SIZE):
			src = sourceIP.replace(".", "")
			xored = long(src) ^ virtual[i]
			physicalInd = int((customHash(str(xored)) & 0x7fffffff) % PHYSICAL_BIT_MAP_SIZE)

			if physical[physicalInd] == 0:
				c += 1
		actual, estimated = findCardinality(sourceIP, c)
		scatter_points[actual] = estimated

	fig = plt.figure()
	gx = scatter_points.keys()
	gy = scatter_points.values()
	plt.scatter(gx, gy, linewidths="1")
	# plt.plot(scatter_points.keys(), scatter_points.values(), marker="o", linewidth=".5")
	plt.title("Virtual Bitmap")
	plt.xlabel("Estimate")
	plt.ylabel("Actual")
	fig.savefig('VirtualBitmap.png', dpi=fig.dpi, bbox_inches='tight')
	#plt.show()


physicalBitMap()
estimateSpread()
