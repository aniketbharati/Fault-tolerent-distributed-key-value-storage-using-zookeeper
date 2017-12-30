>This project is all about making a fault tolerent distributed key-value pair system using zookeeper.

>Consists of 6 files:



>"fclient.py" : This is where the client does all the get and put requests.

>"fmaster.py" : The master server initially at the time of setup.

>"fserver1.py","fserver2.py","fserver3.py" : Are the other server in the cluster which shares the key-value pairs and that makes it distributed.

>"watcher.py" : Keeps watch on the server,if the master server dies it conducts the election choose new leader.

>Look at the attached ppts or report pdfs for more. 
