import socket


#for helpers that don't belong anywhere

class qUtils(object):

  HOSTNAME='127.0.0.1'
  MGR_PORT = 7777
  PROX_PORT = 7778
  FETCH_PORT = 7779
  CACHE_PORT = 7780

  @staticmethod
  def open_listener_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    s.bind((qUtils.HOSTNAME,port))
    s.listen(5)
    return s

  def sendMessage(message, port):
    pass
