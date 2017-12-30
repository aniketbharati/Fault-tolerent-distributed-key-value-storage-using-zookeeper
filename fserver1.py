import socket
from kazoo.client import KazooClient
import time
real="6604"
port="efgh:"+real+":master:server2"
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
data=zk.get('/servers/master')[0]
zk.set('/servers/master',data+ " " +port)
zk.ensure_path("/servers/")
zk.create("/servers/server1",real,None,True)

dic={'eat':'ever','fork':'times','goat':'ever','hick':'kick'}

print "---------------Server1 status:Active---------------"


while True:
    s=socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host=socket.gethostname()
    portno=port.split(':')

    s.bind((host,int(portno[1])))
    s.listen(5)
    c,addr=s.accept()
    print 'connected to client'
    c.send('connection established with server1')  
    users_need=c.recv(1024)
    
    if 'get' in users_need:
	print "comes here"
	val=users_need[4:len(users_need)-1]
	c.send('succesfully fetched from server1:')
        c.send(dic[val])
        
    
    if 'put' in users_need:
    
        key=users_need[4:len(users_need)-1]
        val=key.split(':')
        c.send('successfully added.')
        dic[str(val[0])]=str(val[1])
    
    print "Data held by Server1:\n"
    for key in dic:

	print key,":",dic[key],"\n"
    print "------------------------------------------------------------"

    s.close()
