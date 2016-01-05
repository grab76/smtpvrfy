#!/usr/bin/python

#Python tool to check a range of hosts for SMTP servers that respond to VRFY requests

import socket
import sys
from socket import error as socket_error

if len(sys.argv) != 5:
    print "Usage: ./smtpvrfy.py <uname-file> <ip addr subnet i.e. '192.168.1.'> <host from> <host to>"
    print "i.e. ./smtpvrfy.py unames.txt 192.168.10. 200 210"
    print "Will scan from 192.168.10.200-210 for SMTP VRFY with usernames in file uname.txt"
    sys.exit(0)

#Assign variables
unameFile = sys.argv[1]
subnet = sys.argv[2]
hostFrom = sys.argv[3]
hostTo = sys.argv[4]

#Display variables and range to user
print "Checking SMTP VRFY for usernames in " +unameFile+ " in range " +subnet+hostFrom+ "-" +hostTo

#Read the username file
with open(unameFile) as f:
    unames = f.read().splitlines()

#Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for host in range(int(hostFrom), int(hostTo)+1):
    #Attempt to connect to Socket
    try: 
        c = s.connect((subnet+str(host),25))
        #Read banner, but no not display (Use 'print banner' to display)
        banner=s.recv(1024)
        #print banner
        
        print "\n****************************"
        print "Connected to " +subnet,host

        #Send VRFY requests and print result
        for uname in unames:
            s.send('VRFY ' + uname + '\r\n')
            result = s.recv(1024)
            print result

        print "****************************"
        #Close Socket
        s.close()

    #If error is thrown
    except socket_error as serr:
        print "\nNo SMTP at " +subnet,host
