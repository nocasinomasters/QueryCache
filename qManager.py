#runs the show
import socket
from qUtils import qUtils
import cPickle
import time

class qManager:
  def __init__(self):
  	pass

  def cache(url_list): 
	#ask to qCache if he has the data
    	manager = qUtils.send_message(request,qUtils.CACHE_PORT)
    	web_list = {}
	data = qUtils.recv_message(qUtils.CACHE_PORT)
	if data != 'END' : 
		web_list.update(data) #add data to web_list
	return web_list

while True:
	url_list = qUtils.recv_message(qUtils.MGR_PORT) #receive proxy data 
	print 'RECV %s'%cPickle.loads(url_list)
	test = []
	time.sleep(3)
	qUtils.send_message(cPickle.dumps(test),qUtils.PROX_PORT) #after change for web_list maybe we will need deepcopy (not sure)
