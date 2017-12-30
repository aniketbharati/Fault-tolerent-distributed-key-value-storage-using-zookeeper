from kazoo.client import KazooClient
import time
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

data=zk.get("/servers/master")[0]
zk.ensure_path("/watch/")

zk.create("/watch/watcher","master")

def look():

	m = zk.get_children("/servers")

	if(len(m) < 4):
		
		if "master" in m:
			print "master's up"
			zk.set("/watch/watcher","master")
		
		else:
			
	
			leader = min(m)
			print "selected leader :",leader
			

			if leader==zk.get('/watch/watcher')[0].split(':')[0]:
				pass


			else:
			
			
				port=zk.get('/servers/'+leader)[0]
				
				zk.set("/watch/watcher",str(leader)+':'+port)
				zk.set("/servers/" + leader,data)
			


while(1):
	data1 = zk.get_children("/servers",watch = look())
	time.sleep(2)

	print "running servers : ",data1




