#runs the show
import socket
PORT_PROXY = 1000
PORT_CACHE = 1500
PORT_FETCHER = 5000
class qManager:
  def __init__(self):
  	pass

  def cacheOrFetch(request):
  	#ask to qCache if he has the data
    	manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	cache_adrr = ('',PORT_CACHE) # did not choose a hostname yet and port random
    	manager.connect(cache_adrr)
    	manager.send(request)

    	data = manager.recv(8192) 
	return data

  def setup_Manager():
  	s_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_proxy.bind(('', PORT_PROXY))  # did not choose a hostname yet and port random
        s_proxy.listen(5)
        return s_proxy

  s = setup_Manager()

  while True:
    conn,addr = s.accept() #accept connection from proxy
    request = conn.recv(8192) #receive proxy data (buffer_size = 8192)

    data = cacheOrFetch(request)

    #if yes open a socket and send to proxy
    if data == 'yes' : 
      #conn.sendall() #don't know what to send because i don't know what kind of data we need to give back

    else: #if not open a socket and send to fetcher when we have answer we open a socket and send to proxy
      manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      fetcher_adrr = ('',PORT_FETCHER) # did not choose a hostname yet and port random
      manager.connect(fetcher_adrr)
      manager.send(request)
      data = manager.recv(8192) 

    #conn.sendall(senddata)
    conn.close()
