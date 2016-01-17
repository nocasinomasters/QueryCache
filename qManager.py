import socket
from qUtils import qUtils
import cPickle
import time
import threading

"""
qManager.py

qManager waits for a message on the MGR_PORT, containing a list of
URLs from the proxy. The manager passes the message along to the
cache. When the cache sends a response back, the manager can send
the result back to the proxy.
"""

class qManager(threading.Thread):
  def __init__(self,threadID, request):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.request = request

  def run(self): 
    #ask to qCache if he has the data
    global web_list
    manager = qUtils.send_message(self.request,qUtils.CACHE_PORT)
    if self.request != "!KILLPROXY" :
      while True :
        data = qUtils.recv_message(qUtils.MGR_PORT) 
        if data != 'END' :
          data = cPickle.loads(data)
          web_list.append(data) #add data to web_list
        else : break

if __name__ == '__main__':
  while True:
    #receive proxy data
    url_list = qUtils.recv_message(qUtils.MGR_PORT) 
    web_list = [] 
    pThread = qManager(1,url_list)
    pThread.start()
    pThread.join()
    if url_list == "!KILLPROXY" : break
    print 'FIN THREAD %s'%web_list
    qUtils.send_message(cPickle.dumps(web_list),qUtils.PROX_PORT)
    print 'SEND TO PROXY'
