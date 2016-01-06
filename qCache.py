from qUtils import qUtils
import pickle
import time

# stores objects that have already been gathered from the web and takes it from the web if not


class qCache:
    def __init__(self):
        self.__checkdoc = 0

    myTable = dict()                                                    # Have to change the structure

    def check_cache_object(self, objectName):
        return objectName in qCache.myTable

    def set_cache_object(self, objectName, objectValue):
        qCache.myTable[objectName] = objectValue                        # Have to change how to stock the files

    def get_cache_object(self, objectName):
        return qCache.myTable.get(objectName)

    def setup_cache(self):
        return qUtils.open_listener(qUtils.CACHE_PORT)

    def destroy_cache(self):
        self.myTable.clear()

    def main_cache(self):
        self.setup_cache()
        while True:
            request = pickle.loads(qUtils.recv_message(qUtils.CACHE_PORT))
            print request
            # "Do the urls exist in the cache?"
            while self.__checkdoc < 10:
                    buff = request[self.__checkdoc]
                    if self.check_cache_object(buff):  # Yes, send the local address to the manager
                        print "yes in the cache"
                        ayfile = pickle.dumps([buff,  self.get_cache_object(buff)])
                        qUtils.send_message(ayfile, qUtils.MGR_PORT)  # send the address to the mgr
                    else:                         # No
                        print "not in the cache "
                        qUtils.send_message(buff, qUtils.FETCH_PORT)
                        time.sleep(1)
                        page = qUtils.recv_message(qUtils.FETCH_PORT)       # what does it receive from the fetcher?
                        print page
                        self.set_cache_object(buff, page)

                        anfile = pickle.dumps([buff,  self.get_cache_object(buff)])
                        qUtils.send_message(anfile, qUtils.MGR_PORT)  # send the address to the mgr
                        print "send a file "
                    self.__checkdoc += 1
                    print "documents checked" + str(self.__checkdoc)
            time.sleep(1)
            qUtils.send_message("END", qUtils.MGR_PORT)

if __name__ == '__main__':
    cache = qCache()
    cache.main_cache()