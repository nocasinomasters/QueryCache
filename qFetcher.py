from bs4 import BeautifulSoup
import errno
import socket
import thread
import threading
import urllib2
import os
import re
from qUtils import qUtils 
import time 

"""
qFetcher.py

The fetcher is responsible for downloading http objects if the
system has determined that they are not in the cache. This class
saves objects from the web to disk, re-writes any internal links
in html to point to local objects which have been downloaded, and
finally sends the local file path back to the cache.
"""
class qFetcherThread(threading.Thread):

 def __init__(self,threadID, url):
   threading.Thread.__init__(self)
   self.threadID = threadID
   self.url_to_fetch = url
   self.mainpage = ""
   self.saved_page_dir = ""

 #fetch js and css files
 def fetch_css_and_js(self,resource_type):
   resource_files = []
   if resource_type == 'css':
     resource_files = self.css
   elif resource_type == 'js':
     resource_files = self.js

   for resource in resource_files:
     resource_rel_url = resource.get('src')

     #decline googleapis links, which cause trouble
     if 'googleapis' in str(resource):
       continue

     script_url = self.url_to_fetch + resource_rel_url
     script_data = urllib2.urlopen(script_url).read()
     rel_file_path = os.path.basename(resource_rel_url).split('?')[0]
     file_path = self.saved_page_dir + '/'  + rel_file_path

     with open(file_path, 'w') as f:
       f.write(script_data)

 #each image resource has a downloading thread dispatched
 def fetch_images(self):
   for link in self.imgs:
     thread.start_new_thread(self.fetch_image,(link,))

 #download an image file locally with urllib2
 def fetch_image(self,link):
   img_url = link.get('src')
   if img_url.startswith('/'):
     abs_img_url = self.url_to_fetch + img_url
   else:
     abs_img_url = img_url
   print '-------------------->' + abs_img_url
   self.headers = {"User-Agent" : \
     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"}
   img_req = urllib2.Request(abs_img_url, headers=self.headers)
   img_data = urllib2.urlopen(img_req).read() 
   img_name = filter(str.isalnum,str(abs_img_url))
   img_path = self.saved_page_dir + '/' + img_name
   with open(img_path,'w') as f:
     f.write(img_data)

 #replace internal urls to relative file paths in index.html
 def rewrite_links(self):
   list_of_links = [link.get('src') for link in self.imgs] + \
                   [link.get('href') for link in self.css] + \
                   [link.get('script') for link in self.js]

   for link in list_of_links:
     local_file_name = os.path.basename(link).split('?')[0]
     self.mainpage.replace(link,local_file_name)

 #each webpage gets its own directory to store its files
 def run(self):
   #self.url_to_fetch = qUtils.recv_message(qUtils.FETCH_PORT)
   print 'cache request for url: ' + self.url_to_fetch

   self.saved_page_dir = 'cache/' + filter(str.isalnum, str(self.url_to_fetch))
   try:
     os.mkdir(self.saved_page_dir)
   except OSError as exc:
     if exc.errno == errno.EEXIST and os.path.isdir(self.saved_page_dir):
       pass
     else:
       raise

   #persistent connection would be nice
   response = urllib2.urlopen(self.url_to_fetch)
   self.mainpage = response.read()
   self.soup = BeautifulSoup(self.mainpage,'html.parser')
   self.imgs = list(set(self.soup.find_all('img')))
   self.css = self.soup.find_all('link', rel="stylesheet")
   self.js = self.soup.find_all('script', src=re.compile(".*"))

   with open(self.saved_page_dir + '/index.html','w') as f:
     f.write(self.mainpage)

   #self.fetch_images()
   #self.fetch_css_and_js()
   #self.rewrite_links()

   print 'sending the cache a local file at ' + self.saved_page_dir + '/index.html'
   #qUtils.send_message(self.saved_page_dir+'/index.html', qUtils.CACHE_PORT)

#wait for a fetch request from the cache, then dispatch a fetcher thread
#and finally send the result back to the cache 
if __name__=='__main__':
  while True : 
    #state = False
    #data = ' '
    print 'LISTEN CACHE'
    data = qUtils.recv_message(qUtils.FETCH_PORT)
    if data == "!KILLPROXY":
      break
    pThread = qFetcherThread(5,data)
    pThread.start()
    time.sleep(1)
    pThread.join()
    qUtils.send_message(pThread.saved_page_dir + '/index.html', qUtils.CACHE_PORT)

