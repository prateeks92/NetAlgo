def filereader(algo):
	retMap = dict()
	inputFile = "E:\Projects\\traffic.txt"
	sourceIp = ""
	destIp = ""
	line = ""
	flowSize = 0
	firstLine = True

	try:
		with open(inputFile, 'r') as inFile:
			for line in inFile:
				if firstLine:
					firstLine = False
					continue

				inputArr = line.split("   ")
				count = 0
				for s in inputArr:
					if s == "":
						continue
					if count == 0:
						sourceIp = s.strip()
						count += 1
					else:
						if count == 1:
							destIp = s.strip()
							count += 1
						else:
							if count == 2:
								flowSize = int(s.strip())
								break
				if algo == 1:
					destMap = retMap.get(sourceIp, dict())
					destMap[destIp] = flowSize
					retMap[sourceIp] = destMap
				else:
					if algo == 2:
						destList = retMap.get(sourceIp, [])
						destList.append(destIp)
						retMap[sourceIp] = destList
					else:
						if algo == 3:
							initialFlowSize = retMap.get(sourceIp + destIp, 0)
							flowSize += initialFlowSize
							retMap[sourceIp + destIp] = flowSize

	except Exception as error:
		print error
	return retMap
