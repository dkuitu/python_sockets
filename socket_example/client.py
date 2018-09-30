import sys, socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	lenIn = len(sys.argv) #number of inputs 
	packet = bytearray() #bytearray for 
	datagram = bytearray()
	operand = sys.argv[3]
	if operand == "+":
		datagram.append(2**0)
	if operand == "-":
		datagram.append(2**1)
	if operand == "*":
		datagram.append(2**2)
		
	for i in range(4,lenIn):
		packet.append(int(sys.argv[i]))
	
	packlen = len(packet)
	datagram.append(packlen)
	
	lastByte = None
	if packlen % 2 == 1:
		lastByte = packet[packlen-1]<<4
		packlen -= 1

	i=0
	while i < packlen:
		datagram.append((packet[i] << 4) | packet[i+1])
		i+=2
	if lastByte:
		datagram.append(lastByte)		

	
	s.sendto(datagram, (sys.argv[1], int(sys.argv[2])))
	datagram = bytearray(1024)
	
	bytes = s.recv(1024)

	maskd = 0x000000FF
	maskc = 0x0000FF00
	maskb = 0x00FF0000
	maska = 0xFF000000	
		
	a = ((bytes[0] << 24) & maska)
	b = ((bytes[1] << 16) & maskb)
	c = ((bytes[2] << 8) & maskc)
	d = (bytes[3] & maskd)
	output = a | b | c | d
	if (output > (2**31)-1):
		result = output - 2**32
		print(result)
	else:
		print(output)
