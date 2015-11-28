#!/usr/bin/env python
#LGS SimSuite Client
#Copyright (c) 2015 Filip Marinic

from time import gmtime, strftime, time, sleep
import socket
import math
import sys
import paramiko

#server parameters
server_username = "Pi"
server_password = "********"
server_path = "python /home/pi/server.py" #if server script is compiled then: server_path = "/home/pi/server"


BUFFER_SIZE = 1300
frame_start = 1000000000
legal_ip = False
dest_port = datarate = None

try:
	while legal_ip == False:
		dest_ip = raw_input("\nEnter TM server IP address: ")
		if dest_ip == '' : dest_ip = 'abc'
		else : dest_ip = str(dest_ip)
		try:
			socket.inet_pton(socket.AF_INET,dest_ip)
			legal_ip = True
		except socket.error:
			legal_ip = False
			print "Invalid IP address."
		
	while dest_port < 1025:	
		dest_port = raw_input("\nEnter desired TM port (1024-65535): ")
		if dest_port == '' : dest_port = 0
		else : dest_port = int(dest_port)
		
	while not datarate:	
		datarate = raw_input("\nEnter desired TM datarate in kbps (or 0 for max speed): ")
		try : 
			datarate = int(datarate)
		except :
			datarate = None
		
	print "\nPreparing server... "
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(dest_ip, username=server_username, password=server_password)
	ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("nohup "+str(server_path)+" "+str(dest_port)+" "+str(datarate))#
	sleep(3)
	print "Server ready!"
	while True:
		frames_requested = None
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 240000)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.connect((dest_ip, dest_port))
		except:
			print "Cannot connect to server."
			sys.exit(1)
		while not frames_requested:
			frames_requested = raw_input("\nEnter how many TM frames shall server send (or enter 0 to exit): ")
		frames_requested = int(frames_requested)
		
		if frames_requested > 0 : pass
		else :
			terminate = "terminated"
			s.send(terminate)
			s.shutdown(2)
			s.close()
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("killall server")
			sys.exit(1)

		total_frames = 0
		first_frame_time = 0
				
		MESSAGE = str(frame_start + frames_requested)
		s.send(MESSAGE)
		
		while True:
			packet = s.recv(BUFFER_SIZE, socket.MSG_WAITALL)
			if packet :
				current_frame = packet[:30]
				timestamp = strftime("%d/%m/%Y-%H:%M:%S", gmtime())
				total_frames += 1
				print current_frame, "--> Receive time:", timestamp
				if total_frames == 1 : first_frame_time = time()
			else :
				sleep (0.1)
			if total_frames == frames_requested :
				print '\nTotal TM frames received: ', total_frames
				speed_f = math.ceil((total_frames/(time()-first_frame_time))*100)/100
				speed_b = math.ceil((((total_frames*1300*8)/(time()-first_frame_time))/1000)*100)/100
				print 'Average TM framerate:', speed_f, 'frames/sec'
				print 'Average datarate:', speed_b, 'kbps'
				if datarate > 0 : print '(desired datarate:', datarate, 'kbps)'
				else : print '(desired datarate: max speed)'				
				total_frames = 0
				terminate = "terminated"
				s.send(terminate)
				break


except (KeyboardInterrupt):
	s.close()
	ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("killall server")
	sys.exit(1)
