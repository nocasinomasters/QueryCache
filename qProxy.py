from DDGURLParser import DDGURLParser
import urllib
import urllib2
import socket
import threading
from qUtils import qUtils

class qProxyThread(threading.Thread):

 def __init__(self, threadID):
   threading.Thread.__init__(self)
   self.threadID = threadID

 def setup_proxy_server(self):
   return qUtils.open_listener(qUtils.PROX_PORT)

 @staticmethod
 def parse_request_for_query(request):      # GET /?query=xxx HTTP/1.1\r\n Host: xxx User-Agent: xxx...
   request_lines = request.splitlines()     #["GET /?query=xxx HTTP/1.1", "Host: xxx", "User-Agent: xxx",...]
   req_resource = request_lines[0]          #"GET /?query=xxx HTTP/1.1"
   req_query = req_resource.split(' ')[1]     #/?query=xxx
   search_query = req_query[len("/?query="):] #xxx
 #doesn't handle + character right now
 #urldecoded_query = urllib.unquote(search_query).decode('utf8')
 #search_query_plain = urllib.unquote_plus(urldecoded_query)
 #print search_query
 #print search_query_plain
   return search_query

 @staticmethod
 def execute_search(query):
   #only ddg has non-js for now
   the_req = urllib2.Request('https://duckduckgo.com/html/?q='+query)
   the_response = urllib2.urlopen(the_req)
   the_page = the_response.read()
   return the_page

 @staticmethod
 def parse_results_for_urls(results):
   p = DDGURLParser()
   p.feed(results)
   p.close()
   #print p.data
   return  [x.strip() for x in p.data ]

 def run(self):
   print 'starting proxy server thread'
   s = self.setup_proxy_server()
   while True:
     conn,addr = s.accept()
     request = conn.recv(8192)

     #print request

     # this is the intended way to shut down the proxy thread,
     # the manager will connect and send a !KILLPROXY message
     if request.startswith("!KILLPROXY"):
       conn.close()
       return

     search_query = self.parse_request_for_query(request)

     # this is just temporary workaround to kill the program from the browser
     # until the manager can send real !KILLPROXY commands
     if "KILLPROXY" in search_query:
       conn.close()
       return

     search_results = self.execute_search(search_query) 
     url_list = self.parse_results_for_urls(search_results)

     print url_list
  
     senddata = qUtils.build_standard_response()
     conn.sendall(senddata)
     conn.close()

if __name__ == '__main__':
  pThread = qProxyThread(1)
  pThread.start()
  #print 'made it here'

