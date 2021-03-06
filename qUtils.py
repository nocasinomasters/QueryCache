from email.utils import formatdate
import socket

"""
qUtils.py

for helpers that don't belong anywhere else
"""

class qUtils():

  HOSTNAME='127.0.0.1'
  PROX_PORT = 7776
  MGR_PORT = 7777
  BROWSER_PORT = 7778
  FETCH_PORT = 7779
  CACHE_PORT = 7780

  #returns a socket listening on port
  #the caller then has to accept() on the returned socket
  #classes should not use this directly, it is for this class only
  @staticmethod
  def open_listener(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    s.bind((qUtils.HOSTNAME,port))
    s.listen(5)
    return s

  @staticmethod
  def send_message(message, port):
    #lock = threading.Lock()
    #lock.acquire()
    qUtils.check_port(port)
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((qUtils.HOSTNAME,port))
      s.sendall(message)
      s.close()
      print 'CLOSE SEND'
    except socket.error as serr:
      print str(serr) + ', try again later'
    finally:
      pass
      # lock.release() # release lock, no matter what
  #blocks because of accept; waiting until someone connects
  @staticmethod
  def recv_message(port):
    #lock = threading.Lock()
    #lock.acquire()
    qUtils.check_port(port)
    data = ''
    try:
      s = qUtils.open_listener(port)
      conn, conn_info = s.accept()

      while True:
        newData = conn.recv(1024)
        if not newData:
          break

        data += newData

      conn.close()
      print 'CLOOSSEE RECV'
    finally:
     # lock.release() # release lock, no matter what
      #print data
      return data
    
  @staticmethod
  def check_port(port):
    if port < qUtils.PROX_PORT or port > qUtils.CACHE_PORT:
      raise ValueError('port %r is out of range, choose 7777-7780')

  @staticmethod
  def build_standard_header(content):
    version = "HTTP/1.0"
    status_code = "200"
    resp_phrase = "OK"
    content_type = "text/html"
    

    content_len=str(len(content))
    date = formatdate(timeval=None, localtime=False, usegmt=True)

    CRETURN='\r\n'
    response = version + ' ' + status_code + ' ' + ' ' + resp_phrase + CRETURN + \
                     "Date:" + date + CRETURN + \
                     "Content-Type:" + content_type + CRETURN + \
                     "Content-Length:" + content_len + CRETURN + \
                     CRETURN + \
                     CRETURN

    return response

  @staticmethod
  def build_response(html_file,url_file_map):
    with open(html_file) as f:
      content = f.read()

    if url_file_map != []:
      content = qUtils.add_some_stuff(content, url_file_map)

    return qUtils.build_standard_header(content) + content

  @staticmethod
  def add_some_stuff(content, url_file_map):
    print 'big cntent 888888888888888' + content
    print 'more bs' + str(url_file_map)

  @staticmethod
  def build_standard_response(url_file_map):
    return qUtils.build_response("index.html",url_file_map)

  @staticmethod
  def build_http_request(url):
    return
