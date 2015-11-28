#!/usr/bin/env python
# LGS SimSuite Server
#Copyright (c) 2015 Filip Marinic

from time import sleep, gmtime, strftime
import socket
import math
import sys

TCP_S_IP = '0.0.0.0'

BUFFER_SIZE = 10
FRAME_ID = 1000000000
frames_sent = 0
MESSAGE = "_9HXuFd6BoQGA0t5nvoLfOBUhP9rKGCFKPUG6JvFfBr6zJZDwzHlgTyCoBk04sxPQEaQ20PoeyRtYcZwETCusXclo8K1cvb9eqtc34zAGfF3b4KQDkTv3yobKHwUZUTwiCGXfzqO9gYvFTZAuHJCX2imLo4KzILiyQn97zFAhm2jj8Al4PC6ZKQDveGkO8WMM6EWVOJpjtkpewq7BhknLkqUtYSKUDiEbNShKGn1uzaupMAhtovSgYSsPo6baCnFRD3fy9gxQp8mK63wbeT9umnmrSipY3j9mvyszJviiQnXmkb3kaGrSTuTuVwwQIh7KtYRHORWn0G0rF7irQX9OJVWEQQXFAGc6323QhIfNudhHJgczC2HSyDCjPZG3aqKHYXUL9ndqt66QCgsplXyoSfIf6cZ84lzcN7ssGfG6GJIX6GTQ1bavjhuUvJofdYXF1N2rXONxOtgXcdbGksRcm3fN0gTeqO0l2cnMPRYOAv4s4xHs469tC0xKTsKky5Fu15LXohKIVeW0VyPEr4stZdIqdhfyTXcbLHjNjvXPGt5DM7Z4DS6NCcSwVodcBOrELkACd6SEqwNuMe9HXuFd6BoQGA0t5nvoLfOBUhP9rKGCFKPUG6JvFfBr6zJZDwzHlgTyCoBk04sxPQEaQ20PoeyRtYcZwETCusXclo8K1cvb9eqtc34zAGfF3b4KQDkTv3yobKHwUZUTwiCGXfzqO9gYvFTZAuHJCX2imLo4KzILiyQn97zFAhm2jj8Al4PC6ZKQDveGkO8WMM6EWVOJpjtkpewq7BhknLkqUtYSKUDiEbNShKGn1uzaupMAhtovSgYSsPo6baCnFRD3fy9gxQp8mK63wbeT9umnmrSipY3j9mvyszJviiQnXmkb3kaGrSTuTuVwwQIh7KtYRHORWn0G0rF7irQX9OJVWEQQXFAGc6323QhIfNudhHJgczC2HSyDCjPZG3aqKHYXUL9ndqt66QCgsplXyoSfIf6cZ84lzcN7ssGfG6GJIX6GTQ1bavjhuUvJofdYXF1N2rXONxOtgXcdbGksRcm3fN0gTeqO0l2cnMPRYOAv4s4xHs469tC0xKTsKky5Fu15LXohKIVeW0VyPEr4stZdIqdhfyTXcbLHjNjvXPGt5DM7Z4DS6NCcSwVodcBOrELkACd6SEqwNuMey5Fu15LXohKIVeW0VyPEr4stZdIqdhfyTXcbLHjNjvXPGt5DM7Z4DS6NCcSwVodcBOrELkACd6SEqwNuMejvXPr63"

try:
	try:	
		if len(sys.argv) > 2: 
			TCP_S_PORT = int(sys.argv[1])
			if int(sys.argv[2]) > 0 : period = float(1300/((float(sys.argv[2])*1000)/8)) #Frame size divided by Bytes/s
			else : period = 0
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 240000)
		s.bind((TCP_S_IP, TCP_S_PORT))
		s.listen(True)
	except:
		print "Cannot open port for listening."
		sys.exit(1)
	
	while True:
		conn, addr = s.accept()
		packet = conn.recv(BUFFER_SIZE, socket.MSG_WAITALL)
		if packet :
			received_message = packet[:10]
			if received_message == "terminated":
				conn.close()
				frames_requested = 0
			else : 
				frames_requested = int(received_message) - 1000000000
		else : frames_requested = 0
		timestamp = strftime("%d/%m/%Y-%H:%M:%S", gmtime())
		if frames_requested > 0 :
			print "\nFrames requested: ", frames_requested
			print "Initiating transfer..."
			while ((FRAME_ID - 1000000000) < frames_requested):
				FRAME_ID += 1
				timestamp = "_" + strftime("%d/%m/%Y-%H:%M:%S", gmtime())
				PACKET = str(FRAME_ID) + timestamp + MESSAGE
				frames_sent += 1
				conn.send(PACKET)
				sleep(period)
			print "Total frames sent: ", frames_sent
			frames_requested = 0
			FRAME_ID = 1000000000
			frames_sent = 0
			
except (KeyboardInterrupt):
	conn.close()
	s.close()
	sys.exit(1)
