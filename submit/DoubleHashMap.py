import matplotlib
matplotlib.use('Agg')
from fileRead import filereader
import matplotlib.pyplot as plt


def DoubleHashM():
	flowMap = filereader(1)
	plot_points = dict()

	with open('dhmOut.txt', 'w') as outFile:
		for flow in flowMap.keys():
			estimated = len(flowMap[flow])
			actual = estimated
			plot_points[actual] = estimated
			outFile.write(str(flow) + "\t\t" + str(actual) + "\t\t" + str(estimated) + "\n")
	outFile.close()

	fig = plt.figure()
	plt.title("Double Hash Map")
	plt.xlabel("Estimate")
	plt.ylabel("Actual")
	plt.plot(plot_points.keys(), plot_points.values(), marker="o", linewidth=".5")
	fig.savefig('DoubleHashMap.png', dpi=fig.dpi, bbox_inches='tight')
	plt.show()

DoubleHashM()
