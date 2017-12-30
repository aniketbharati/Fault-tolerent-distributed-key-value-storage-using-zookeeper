import socket
from kazoo.client import KazooClient
import time
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
print "---------------Client status:Active---------------"

allservers=['master','server1','server2','server3']

def checkup(l):

	flag=0
	port=0
	alive=zk.get_children("/servers")
	#print "printing alive :",alive
	#print l
	n=0
	if(len(alive)==4):
		port=l[1]
		#print "port here :",port
	else:
		#print "checkup initial"
		

		for y in allservers:
			if y not in l[2:] and y in alive:
				#print "y here",y
				
				if y=="master":
					
					val=zk.get('/servers/master')[0]
					
					data=val.split(' ')[0].split(':')[1]
					#print "data :",data
					port=int(data)
					return port
					break
				else:
					if zk.get('/watch/watcher')[0].split(':')[0]==y:
						port=int(zk.get('/watch/watcher')[0].split(':')[1])
						return port
					else:
						port=zk.get('/servers/'+y)[0]
						return port
		for i in l[2:]:
			if i in alive:
			
				#print "starting from :",i
				try:
					if i=="master":
						#print "in i try"
						val=zk.get('/servers/'+i)[0]
						data=val.split(' ')[0].split(':')[1]
						#print "data :",data
						port=int(data)
						return port
						break
					
					else:
						if zk.get('/watch/watcher')[0].split(':')[0]==i:
							port=int(zk.get('/watch/watcher')[0].split(':')[1])
							return port
						else:
							#print "checking now:",i
							val=zk.get('/servers/'+i)[0]
							#print "val :",val
							port=int(val)
							#print "port in try :",port
							flag=1
							#print "inside try"
							#print "breaking now"
							break
				except:
					#print "passing now"
					pass
				
		
				finally:
					pass
				

	print "returning port now :", port				
	return port	

	
while True:

    up=zk.get('/watch/watcher')[0].split(':')[0]
    print "leader : ", up
    data=zk.get('/servers/' + up)[0]
    #print "data",data

    s=socket.socket()
  

    host=socket.gethostname()

    
    i=raw_input()
    val=i[4:len(i)-1]
    
    if "get" in i:
	
	for x in data.split(' '):
		#print "in the get for loop"
		part=x.split(':')
		if val[0] in part[0]:
			#print "before checkup call"
			port=checkup(part)
			break

	s.connect((host,int(port)))
	s.send(i)
	print s.recv(1024)
	print s.recv(1024)
	print s.recv(1024)
	s.close()
        print "------------------------------------------------------------"
	

	
    if "put" in i:
	try:
		n=socket.socket()
	
		for x in data.split(' '):
			part=x.split(':')
			if val[0] in part[0]:

				port=checkup(part)
			
				break

		n.connect((host,int(port)))
		n.send(i)
		print n.recv(1024)
		n.close()
	except:
		pass
	
	for x in data.split(' '):
		part=x.split(':')
		if val[0] in part[0]:
			l=[part[2],part[3]]
	
			break
	
	for x in l:
		print "sending replication values to:",x,"\n"
    	for x in l:
	
			m=socket.socket()
			if x=="master":
				port=int(data.split(':')[1])
				try:
					m.connect((host,port))
					m.send(i)
                        		print m.recv(1024)
					m.close()
				except:

					pass
		


			else:
				
	
     				try:
					adr=int(zk.get('/servers/'+x)[0])
					m.connect((host,adr))
					m.send(i)
					print m.recv(1024)
					m.close()
				except:	
					print "detecting server failure"
					pass
        print "------------------------------------------------------------"
	
