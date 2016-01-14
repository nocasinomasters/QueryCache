import subprocess
import time
pFetch = subprocess.Popen(['python','qProxy.py'])
#time.sleep(1)
pManager = subprocess.Popen(['python','qManager.py'])
#time.sleep(1)
pCache = subprocess.Popen(['python','qCache.py'])
#time.sleep(1)
pProxy = subprocess.Popen(['python','qFetcher.py'])
