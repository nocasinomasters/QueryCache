import unittest
import socket
import qCache

PORT_MANAGER = 5000

#python TestCache.py

class TestCache(unittest.TestCase):

  #called before every test
  def setUp(self):
    self.myCache = qCache()
    self.myKey = "yahoo.com"
    self.myValue = "lots of html"

  #called after every test
  def tearDown(self):
    self.myCache.destroyCache()
    self.myCache = None


  #direct cache calls with no network

  def test_local_cache_get_set(self):
    self.set_cache_object(key,value)
    newValue = self.get_cache_object(key)
    self.assertEqual(value,newValue)

  def test_local_cache_check(self):
    self.set_cache_object(key,value)
    present = check_cache_object(key)
    self.assertTrue(present)

  #indirect cache calls over sockets

  def test_remote_cache_check(self):
    outside_caller_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    outside_caller_socket.bind(('',PORT_MANAGER))
    outside_caller_socket.sendall('http://yahoo.com')
    response = outside_caller_socket.receive(1024)
    outside_caller_socket.close()
    self.assertFalse(response)

 
  #as of now, this depends on fetcher working!
  def test_remote_cache_get_set(self):
    #set yahoo.com in the cache..
    outside_caller_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    outside_caller_socket.bind(('',PORT_MANAGER))
    outside_caller_socket.sendall('sc http://yahoo.com')

    #then get it (better assertion needed..)
    outside_caller_socket.sendall('gc http://yahoo.com')
    response = outside_caller_socket.receive(8192)
    outside_caller_socket.close()
    self.AssertIsNotNone(response)



if __name__ == '__main__':
    unittest.main()
