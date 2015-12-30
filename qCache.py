import socket

# stores objects that have already been gathered from the web
# do we set a limit size for the cache?
PORT_MANAGER = 2000
PORT_FETCHER = 5000


class qCache:

    def __init__(self):
        pass

    myTable = dict()

    def check_cache_object(objectName):
        return objectName in qCache.myTable

    def set_cache_object(objectName, objectValue):
        qCache.myTable["url"] = objectName
        qCache.myTable["attribute"] = objectValue

    def get_cache_object(objectName):
        return qCache.myTable.get(objectName)

    def setup_cache():
        s_manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_manager.bind(('', PORT_MANAGER))  # did not choose a hostname yet and port random
        s_manager.listen(5)
        return s_manager

    def destroy_cache():
        self.myTable.clear()

    sman = setup_cache()
    print('lala')
    while True:
        conn, conn_info = sman.accept()
        request = conn.recv(1024)
        if request.startswith('http'):
            buff = request
            conn.send(check_cache_object(request))
            conn.close()
        elif request.startswith('gc') and 'buff' in locals():
                conn.send(get_cache_object(buff))
        elif request.startswith('sc') and 'buff' in locals():
            s_fetcher = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_fetcher.connect('localhost', PORT_FETCHER)
            page = s_fetcher.recv(8192)
            set_cache_object(buff, page)
            s_fetcher.close()
