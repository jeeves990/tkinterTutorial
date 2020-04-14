# -*- coding: utf-8 -*-
"""
https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/

@author: FBA_S
"""

import sys 
import trace 
import threading 
import time 
import os


class thread_with_trace(threading.Thread): 
  def __init__(self, *args, **keywords): 
    self.pid = os.getpid()
    threading.Thread.__init__(self, *args, **keywords) 
    self.killed = False
  
  def start(self): 
    self.__run_backup = self.run 
    self.run = self.__run       
    threading.Thread.start(self) 
  
  def __run(self): 
    #gettrace = getattr(sys, 'gettrace', None)
    #print('gettrace is: [{}]'.format(gettrace))
    sys.settrace(self.globaltrace) 
    self.__run_backup() 
    self.run = self.__run_backup 
  
  def globaltrace(self, frame, event, arg): 
    if event == 'call': 
      return self.localtrace 
    else: 
      return None
  
  def localtrace(self, frame, event, arg): 
    if self.killed: 
      if event == 'line': 
        raise SystemExit() 
    return self.localtrace 
  
  def kill(self): 
    self.killed = True
  
def func(): 
    while True: 
        ltm = time.localtime()
        S = "%s%2.2d:%2.2d:%2.2d pid: [%d]" % ('thread running', int(ltm[3]), int(ltm[4]), int(ltm[5], pid))
        print(S) 
  

if __name__ == '__main__':
    t1 = thread_with_trace(target = func) 
    t1.start() 
    time.sleep(2) 
    t1.kill() 
    t1.join() 
    if not t1.isAlive(): 
      print('thread killed') 

