import unittest
import pickle
import time
import socket
from qUtils import qUtils
from qCache import qCache



#python TestCache.py

class TestCache(unittest.TestCase):

  #called before every test
  def setUp(self):
    self.myCache = qCache()
    self.myKey = "yahoo.com"
    self.myValue = "lots of html"

  #called after every test
  def tearDown(self):
    self.myCache.destroy_cache()
    self.myCache = None


  #direct cache calls with no network

  def test_local_cache_get_set(self):
    self.myCache.set_cache_object(self.myKey, self.myValue)
    newValue = self.myCache.get_cache_object(self.myKey)
    self.assertEqual(self.myValue, newValue)

  def test_local_cache_check(self):
    self.myCache.set_cache_object(self.myKey, self.myValue)
    present = self.myCache.check_cache_object(self.myKey)
    self.assertTrue(present)

  #indirect cache calls over sockets

  def test_remote_cache_check(self):
    arr = pickle.dumps(['http://yahoo.com','http://yahoo.com','3'])
    qUtils.send_message(arr, qUtils.CACHE_PORT)
    #self.myCache.main_cache()
    print "foo"
    response = qUtils.recv_message(qUtils.FETCH_PORT)
    print response
    time.sleep(3)
    qUtils.send_message('/localpath/tothe/file/yahoo', qUtils.FETCH_PORT)

    response2 = pickle.loads(qUtils.recv_message(qUtils.MGR_PORT))
    print response2

    response3 = qUtils.recv_message(qUtils.MGR_PORT)
    print response3
    # outside_caller_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # outside_caller_socket.bind(('',PORT_MANAGER))
    # outside_caller_socket.sendall('http://yahoo.com')
    # response = outside_caller_socket.receive(1024)
    # outside_caller_socket.close()

  # #as of now, this depends on fetcher working!
  # def test_remote_cache_get_set(self):
  #
  #   #set yahoo.com in the cache..
  #   qUtils.send_message('the html file', qUtils.CACHE_PORT)
  #   response = qUtils.open_listener(qUtils.MGR_PORT)
  #   # outside_caller_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  #   # outside_caller_socket.bind(('',PORT_MANAGER))
  #   # outside_caller_socket.sendall('sc http://yahoo.com')
  #
  #   #then get it (better assertion needed..)
  #
  #   # outside_caller_socket.sendall('gc http://yahoo.com')
  #   # response = outside_caller_socket.receive(8192)
  #   # outside_caller_socket.close()
  #   self.AssertIsNotNone(response)



if __name__ == '__main__':
    unittest.main()
