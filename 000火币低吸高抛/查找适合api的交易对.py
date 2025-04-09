# -*- coding: UTF-8 -*-
from urllib import request, parse
from urllib.parse import quote

import re
import time
import sys
import json

import hashlib
import hmac
import base64


#import urllib

#============================时间到强制结束线程
import threading
import inspect
import ctypes

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

#=============================

if __name__ == "__main__":

    with open('火币交易对.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ddd=json.loads(f.read())

    ttt=[]
    for dd in ddd["data"]:
        #if dd["quote-currency"]=="usdt" and dd["symbol-partition"]=="main" and dd["state"]=="online" and dd["api-trading"]=="enabled":
        if dd["quote-currency"]=="usdt" and dd["state"]=="online" and dd["api-trading"]=="enabled":
            #ttt.append(dd["symbol"])
            ttt.append(dd)


    #ttt.sort()
    print(len(ttt))
    numm=0
    for tt in ttt:
        if tt['base-currency']+tt['quote-currency']!=tt['symbol']:
            print(tt['symbol'])

        if tt["value-precision"]==8:
            numm+=1
    print(f"value-precision: {numm}")

    numm=0
    for tt in ttt:
        if tt["min-order-value"]==5:
            numm+=1
    print(f"min-order-value: {numm}")
    
    with open('api交易对.txt', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(json.dumps(ttt, indent=4)+"\r\n")

