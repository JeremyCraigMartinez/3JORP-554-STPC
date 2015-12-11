# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 13:21:42 2015

@author: samue_000
"""

#!/usr/bin/python

import Queue
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.q)
        print "Exiting " + self.name
        
        

def process_data(threadName, q):
    
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)
        # Have to lock the queue to get or put.
        queueLock.acquire()
        #puts an element into the queue
        commQueue.put("HTML Data from %s" % (threadName))
        #release the queue
        queueLock.release()
        

threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
commQueue = Queue.Queue(10) # slave to master queue could make one for each thread
threads = []
threadID = 1

# Create new threads
for task in nameList:
    thread = myThread(threadID, task, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the work queue
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()




while not workQueue.empty():
    pass

exitFlag = 1

# Listen For responses
while not commQueue.empty():
    queueLock.acquire()
    master_data = commQueue.get()    
    print "%s" % (master_data)
    queueLock.release()
else:
    pass
time.sleep(1)




# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"