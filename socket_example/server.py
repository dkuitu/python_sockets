import sys, socket

while True:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', int(sys.argv[1])))

	datagram, address = s.recvfrom(1024)
	if (datagram, address):
		datlen = len(datagram)
		numoper = datagram[1]
		print("%d " %numoper)
		index = 0
		operands = bytearray()
		rightGate = 15
		leftGate = 240
		lastByte = None
		oddFlag = False

		i=2
		if numoper % 2 == 1:
			oddFlag = True
			lastByte = datagram[datlen-1]>>4
			numoper -= 1
		while index < numoper:
			operands.append((datagram[i]&leftGate)>>4)
			index += 1
			operands.append(datagram[i]&rightGate)
			index += 1
			i+=1
		if oddFlag:
			operands.append(lastByte)

		output = operands[0]
		print(datagram[0])
		if datagram[0] == 2**0:
			for j in range(1,len(operands)):
				output += operands[j]
		if datagram[0] == 2**1:
			for j in range(1,len(operands)):
				output -= operands[j]
		if datagram[0] == 2**2:
			for j in range(1,len(operands)):
				output *= operands[j]

		maskd = 0x000000FF
		maskc = 0x0000FF00
		maskb = 0x00FF0000
		maska = 0xFF000000

		bytes = bytearray()
		bytes.append((output&maska)>>24)
		bytes.append((output&maskb)>>16)
		bytes.append((output&maskc)>>8)
		bytes.append(output&maskd)

		print(output)
		s.sendto(bytes, address)
		s.close()
