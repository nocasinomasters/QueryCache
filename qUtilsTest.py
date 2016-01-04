import unittest
import socket
import threading
import time
from qUtils import qUtils

#python TestUtils.py

class recvThread(threading.Thread):

  def __init__(self, port):
    threading.Thread.__init__(self)
    self.port = port
    self.dataRecvd = ''

  def run(self):
    print 'starting server thread'
    self.dataRecvd = qUtils.recv_message(self.port)
    return

class sendThread(threading.Thread):

  def __init__(self, port, message):
    threading.Thread.__init__(self)
    self.port = port
    self.message = message

  def run(self):
    print 'starting client thread'
    qUtils.send_message(self.message,self.port)
    return


class TestUtils(unittest.TestCase):

  #called before every test
  def setUp(self):
    pass

  #called after every test
  def tearDown(self):
    pass

  def testSending(self):
    myMessage = 'this is my message'
    s = recvThread(qUtils.MGR_PORT)
    c = sendThread(qUtils.MGR_PORT,myMessage)
    s.start()
    time.sleep(0.5) #need some better synchronization
    c.start()
    c.join()
    s.join()
    self.assertEqual(s.dataRecvd,myMessage)

if __name__ == '__main__':
    unittest.main()
