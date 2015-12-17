from email.utils import formatdate
from DDGURLParser import DDGURLParser
import urllib
import urllib2
import socket

HOSTNAME='127.0.0.1'
PORT = 8080
CRETURN='\r\n'

def setup_proxy_server():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
  s.bind((HOSTNAME,PORT))
  s.listen(5)
  return s

def build_response(version,status_code,resp_phrase,content_type,html_file):
  with open(html_file) as f:
    content = f.read()

  content_len=str(len(content))
  date = formatdate(timeval=None, localtime=False, usegmt=True)
  response = version + ' ' + status_code + ' ' + ' ' + resp_phrase + CRETURN + \
             "Date:" + date + CRETURN + \
             "Content-Type:" + content_type + CRETURN + \
             "Content-Length:" + content_len + CRETURN + \
             CRETURN + \
             CRETURN + \
             content
  return response

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

def execute_search(query):
  #only ddg has non-js for now
  the_req = urllib2.Request('https://duckduckgo.com/html/?q='+query)
  the_response = urllib2.urlopen(the_req)
  the_page = the_response.read()
  return the_page

def parse_results_for_urls(results):
  p = DDGURLParser()
  p.feed(results)
  p.close()
#  print p.data
  return  [x.strip() for x in p.data ]

def build_standard_response():
  return build_response("HTTP/1.0","200","OK","text/html","index.html")

s = setup_proxy_server()

while True:
  conn,addr = s.accept()
  request = conn.recv(8192)

  search_query = parse_request_for_query(request)

  search_results = execute_search(search_query) 

  url_list = parse_results_for_urls(search_results)

  print url_list
  
  senddata = build_standard_response()

  conn.sendall(senddata)
  conn.close()



