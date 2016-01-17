import subprocess
import time

"""
qLaunch.py

launcher script for QueryCache
"""
pFetch = subprocess.Popen(['python','qProxy.py'])
pManager = subprocess.Popen(['python','qManager.py'])
pCache = subprocess.Popen(['python','qCache.py'])
pProxy = subprocess.Popen(['python','qFetcher.py'])
