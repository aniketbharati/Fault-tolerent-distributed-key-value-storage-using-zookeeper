import socket
from kazoo.client import KazooClient
import time
real="6638"
port="mnop:"+real+":server1:server2"
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
data=zk.get('/servers/master')[0]
zk.set('/servers/master',data+ " " +port)
zk.ensure_path("/servers/")
zk.create("/servers/server3",real,None,True)

dic={'man':'go','nano':'tech','oxy':'gen','pen':'cil'}


portno=port.split(':')

print "---------------Server3 status:Active---------------"

while True:
    s=socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host=socket.gethostname() 
    s.bind((host,int(portno[1])))
    s.listen(5)
    c,addr=s.accept()
    print 'connected to client'
    c.send('connection established with server3')

    users_need=c.recv(1024)
    
    if 'get' in users_need:
	print "comes here"
	val=users_need[4:len(users_need)-1]
	c.send('succesfully fetched from server3:')
        c.send(dic[val])
        
    
    if 'put' in users_need:
    
        key=users_need[4:len(users_need)-1]
        val=key.split(':')
        c.send('successfully added.')
        dic[str(val[0])]=str(val[1])

    print "Data held by Server3:\n"
    for key in dic:
	
	print key,":",dic[key],"\n"
    print "------------------------------------------------------------"

    s.close()
