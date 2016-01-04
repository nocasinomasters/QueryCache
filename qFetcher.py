import socket
import threading
import urllib2

#gathers objects from the web
class qFetcherThread(threading.Thread):

 def __init__(self,threadID, url):
   threading.Thread.__init__(self)
   self.threadID = threadID
   self.url_to_fetch = url
   self.webdata = ""

 def run(self):
   # change this to only fetch when an internal QueryCache message is received
   response = urllib2.urlopen(self.url_to_fetch)
   self.webdata = response.read() 

if __name__=='__main__':
  qThread = qFetcherThread(2,"http://yahoo.com")
  qThread.start()
  qThread.join()
  print qThread.webdata
   


