from decimal import Decimal
from fileRead import filereader
import hashlib
import random


global BIT_MAP_WIDTH
BIT_MAP_WIDTH = 30000000

global nHashes
nHashes = 5


global bitmap
bitmap = [0]*BIT_MAP_WIDTH


def customHash(s):
	digestMethod = hashlib.sha256()
	digestMethod.update(s)
	return int(digestMethod.hexdigest(), 16)


def BloomFilter():
	global bit_map
	flowMap = filereader(2)
	plot_points = dict()

	for src in flowMap.keys():

		for desti in flowMap[src]:

			for i in range(0, nHashes):
				index = customHash(src + desti + str(i)) % BIT_MAP_WIDTH
				bitmap[index] = 1

	falsePositive = 0
	trueNegative = 0

	for i in range(0, 10000):
		randIP = str(random.randint(0, 256))+"." + str(random.randint(0, 256))+"." + (
				str(random.randint(0, 256))+"." + str(random.randint(0, 256)))
		mem = 1

		for j in range(0, nHashes):
			val = customHash(randIP+str(j))
			mem &= bitmap[val % BIT_MAP_WIDTH]

		if mem == 0:
			trueNegative += 1
		else:
			falsePositive += 1

	print trueNegative, falsePositive, (Decimal(falsePositive)/Decimal(falsePositive+trueNegative))


BloomFilter()







