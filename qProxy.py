#from DDGURLParser import DDGURLParser
from bs4 import BeautifulSoup
import urllib
import urllib2
import socket
import threading
from qUtils import qUtils
import cPickle
import time

class qProxyManager(threading.Thread):

 def __init__(self, threadID,query, threadLock):
   threading.Thread.__init__(self)
   self.threadID = threadID
   self.search_query= query
   self.threadLock = threadLock
 @staticmethod
 def execute_search(query):
   #only ddg has non-js for now
   the_req = urllib2.Request('https://duckduckgo.com/html/?q='+query)
   the_response = urllib2.urlopen(the_req)
   the_page = the_response.read()
   return the_page

 @staticmethod
 def parse_results_for_urls(results):
   soup = BeautifulSoup(results,'html.parser')
   links = list(set([ x.get('href') for x in soup.findAll('a') ]))
#   print links
   external_links =  [x for x in links if str(x).startswith('http')]
   return external_links

 def run(self):
   print 'SECOND Thread'
   print 'QUERY 2 %s' %self.search_query
   search_results = self.execute_search(search_query)
   url_list_tmp = list(set(self.parse_results_for_urls(search_results)))
   url_list = []
   for i in range (0,len(url_list_tmp)) :
     if i == 10 : break
     url_list.append(url_list_tmp[i])
   print 'LIST %s'%url_list

   if url_list != [] :
     self.threadLock.acquire()
     qUtils.send_message(cPickle.dumps(url_list),qUtils.MGR_PORT)
     print 'SEND to MGR'
     data = cPickle.loads(qUtils.recv_message(qUtils.PROX_PORT))
     print 'RECV %s'%data
     self.threadLock.release()

if __name__ == '__main__':
  threadLock = threading.Lock()
  search_query = ' '
  s = qUtils.open_listener(qUtils.BROWSER_PORT)
  def parse_request_for_query(request):      # GET /?query=xxx HTTP/1.1\r\n Host: xxx User-Agent: xxx...
    request_lines = request.splitlines()     #["GET /?query=xxx HTTP/1.1", "Host: xxx", "User-Agent: xxx",...]
    req_resource = request_lines[0]          #"GET /?query=xxx HTTP/1.1"
    req_query = req_resource.split(' ')[1]     #/?query=xxx
    search_query = req_query[len("/?query="):] #xxx
    return search_query
  print 'starting proxy '
  while True:  
    conn,addr = s.accept()
    request = conn.recv(8192)
    print request
    search_query = parse_request_for_query(request)
    print 'QUERY %s'%search_query
    senddata = qUtils.build_standard_response()
    conn.sendall(senddata)  

    if "KILLPROXY" in search_query:
      qUtils.send_message("!KILLPROXY", qUtils.MGR_PORT)
      break

    pThread = qProxyManager(1,search_query,threadLock)
    pThread.start()
    ###pThread.join()
  conn.close()
