from qUtils import qUtils
import pickle
import time
import threading

# stores objects that have already been gathered from the web and takes it from the web if not

class qCacheManager(threading.Thread):
    def __init__(self,threadID,request):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.request = request

    global myTable                                                    # Have to change the structure

    def run(self):
        qUtils.send_message(self.request, qUtils.MGR_PORT)  # send the address to the mgr

class qCacheFetcher(threading.Thread):
    def __init__(self,threadID,request):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.request = request
	
    global myTable                                                    # Have to change the structure
    	
    def set_cache_object(self, objectName, objectValue):
        myTable[objectName] = objectValue                        # Have to change how to stock the files

    def destroy_cache(self):
        myTable.clear()

    def run(self):
	print "not in the cache "
        qUtils.send_message(self.request, qUtils.FETCH_PORT)
        if self.request == "!KILLPROXY" or self.request == 'END' : print 'END' 
	else:
	    print 'WAITING ANSWER FETCHER'
	    page = qUtils.recv_message(qUtils.CACHE_PORT)       # what does it receive from the fetcher?
            print page
            self.set_cache_object(self.request, page)
            anfile = pickle.dumps([self.request, page])
            pThread = qCacheManager(1,anfile)
            pThread.start()
            pThread.join()
            print "send a file "

if __name__ == '__main__':
    myTable = dict()                  # Have to change the structure
    while True:
        url_list = qUtils.recv_message(qUtils.CACHE_PORT)
        if url_list == "!KILLPROXY" : 
	    pThread = qCacheFetcher(2,url_list)
            pThread.start()
	    pThread.join()	
	    break
	else: url_list = pickle.loads(url_list)
        print 'TABLE %s' %myTable
    
        def check_cache_object(objectName):
            return objectName in myTable

        def get_cache_object(objectName):
            return myTable.get(objectName)
        #i = 0
        for url in url_list : 	      #take url
	    #i +=1	
	    #if i == 10 : 
	    #    pThread = qCacheFetcher(4,'END')
            #    pThread.start()
            #    pThread.join()
            #    break	
	    if check_cache_object(url):  # Yes, send the local address to the manager
                print "yes in the cache"
                ayfile = pickle.dumps([url, get_cache_object(url)])
                pThread = qCacheManager(1,ayfile)
                pThread.start()
                pThread.join()
            else:
	        pThread = qCacheFetcher(2,url)
                pThread.start()
                pThread.join()
        print 'FIN THREAD %s'%myTable
        qUtils.send_message("END", qUtils.MGR_PORT)    

