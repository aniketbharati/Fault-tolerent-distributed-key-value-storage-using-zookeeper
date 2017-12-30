import socket
from kazoo.client import KazooClient
import time
port="abcd:6067:server1:server2"
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
zk.ensure_path("/servers/")
zk.create("/servers/master",port,None,True)

dic={'anonymous':'ever','bank':'times','could':'ever','dump':'kick'}

print "---------------Master server status:Active---------------"


while True:
    s=socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host=socket.gethostname()
    portno=port.split(':')

    s.bind((host,int(portno[1])))
    s.listen(5)
    c,addr=s.accept()
    print 'connected to client'
    c.send('connection established with master\n')
    users_need=c.recv(1024)
    
    if 'get' in users_need:
	
	val=users_need[4:len(users_need)-1]
	c.send('succesfully fetched from master server:')
        c.send(dic[val])
        
    if 'put' in users_need:
    
        key=users_need[4:len(users_need)-1]
        val=key.split(':')
        c.send('successfully added.')
        dic[str(val[0])]=str(val[1])

    print "Data held by Master:\n"
    for key in dic:
	
	print key,":",dic[key],"\n"
    print "------------------------------------------------------------"

    s.close()
