import socket


#for helpers that don't belong anywhere

class qUtils(object):

  HOSTNAME='127.0.0.1'
  MGR_PORT = 7777
  PROX_PORT = 7778
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
    qUtils.check_port(port)

    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((qUtils.HOSTNAME,port))
      s.send(message)
      s.close()
    except socket.error as serr:
      print str(serr) + ', try again later'

  #blocks because of accept; waiting until someone connects
  @staticmethod
  def recv_message(port):
    qUtils.check_port(port)

    s = qUtils.open_listener(port)
    conn, conn_info = s.accept()
    data = ''

    while True:
      newData = conn.recv(1024)
      if not newData:
        break

      data += newData

    conn.close()
#    print data
    return data

  @staticmethod
  def check_port(port):
    if port < qUtils.MGR_PORT or port > qUtils.CACHE_PORT:
      raise ValueError('port %r is out of range, choose 7777-7780')


