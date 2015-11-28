# LGS SimSuite

LGS SimSuite is a client-server tool for generating TCP traffic with simulated Space Telemetry Frames. The intended users are network admins who want to validate the network by simulating the production TCP traffic.

A typical business case:  
You are a network admin and you need to setup the network so that some new application at a remote location can properly communicate with another application that runs at your local network. The setup may require new firewall rules, maybe a Qos class for DSCP marking on the WAN, some shaping or policing, or even updates to the routing. If you cannot use the real applications to test everything end to end, there is always a chance that the network won't work (yeah, probably that long forgotten ACL). Then without testing, you let your users know that the network is ready. Some hours later they call you back and report that it isn't, and now you have to troubleshoot under pressure. When you finally find the culprit, you apply the first solution that comes to your mind just because the users want the network to start working immediately. To prevent such cases, I created this simple tool.

Since I work in the space business, the primary goal of this tool is to simulate the Space Link Extension (SLE) telemetry frames for validating the network before any complex Space Applications are even tried. The payload in the frames generated by the tool is a repeating string of random characters (not real telemetry data). However, the tool is suitable for simulating any other type of applications based on TCP. The packet size is fixed to 1300 bytes. 

INSTRUCTIONS: 

You will need Linux, Python 2.7+ and the Paramiko module (pip install paramiko).

Server.py - the script should be copied to a linux machine at the remote location (in my case the remote locations are Ground Stations or  portable Ground Station models which may be deployed literally anywhere on the planet). Cheap Raspberry PIs are best suited to act as servers. You can easily send them anywhere and also easily replace them if they break down. The server script is activated by the client script via SSH, so the server side does not need to be run manually.

Client.py - this script should be placed on a linux machine locally (in my case, this is the control centre). The client script starts/stops the server script via SSH (with the excellent Paramiko module). You will only need to configure the SSH credentials and the full path to the server.py script. When started, the client script will ask for the IP address of the server, the TCP source port from which the server script will send the generated traffic and the desired transfer rate. The client script will then SSH to the server and initiate the server script. Finally it will ask how many frames the server should send and trigger the server to start sending frames. For each received frame it will show the time when the server sent the frame and the time the frame was received by the client. Once all frames are transferred, it will report the average transfer speed.


For the best performance on the Rasberry PIs, I always compile the code by converting the server.py script with Cython to C and then compiling the resulting .c file with gcc:

cython --embed server.py

gcc $CFLAGS -I/usr/include/python2.7 -o server server.c -lpython2.7 -lpthread -lm -lutil -ldl
