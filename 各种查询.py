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

def htmll(url, data=None):     #请求页面，这个函数要用线程，长时间不响应就杀死线程，参数5秒有时不起作用
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36', \
               'X-MBX-APIKEY': API_Key}
        
    try:
        if data:
            data=data.encode('utf-8')
        req = request.Request(url, data, headers=headers)
        #resp = request.urlopen(req,timeout=25)
        with request.urlopen(req, timeout=3) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(e)
        return ""

def exch_timee():  #交易所时间
    global ab_time
    kk="https://api.binance.com/api/v3/time"
    html=htmll(kk)
    try:
        tt=json.loads(html)
        lock.acquire()
        ab_time=int(time.time()*1000)-tt["serverTime"]
        lock.release()
    except Exception as e:
        print(e)
        pass

def assett():  #获取账户各币种余额
    html=htmll(exch_bb())
    try:
        tt=json.loads(html)
        for t in tt["balances"]:
            print(t)
    except Exception as e:
        print(e)
        pass
    finally:
        pass

def all_orderr(a):  #查询历史订单
    kk=exch_dd(a+B_coin_name)
    print(kk)
    html=htmll(kk)
    #print(html)
    if html!="":
        try:
            tt=json.loads(html)
            for t in tt:
                print(t)
        except Exception as e:
            pass

def exch_bb():     #查询指定账户余额
    uu="https://api.binance.com/api/v3/account"
    uu2="recvWindow=5000&timestamp="+str(int(time.time()*1000)-ab_time)
    signature = hmac.new(Secret_Key.encode(encoding = "utf-8"), uu2.encode(encoding = "utf-8"), digestmod=hashlib.sha256).hexdigest()
    return uu+"?"+uu2+"&signature="+signature

def exch_dd(symbol):     #查询历史订单
    uu="https://api.binance.com/api/v3/allOrders"
    uu2="symbol="+symbol+"&limit=20&recvWindow=5000&timestamp="+str(int(time.time()*1000)-ab_time)
    signature = hmac.new(Secret_Key.encode(encoding = "utf-8"), uu2.encode(encoding = "utf-8"), digestmod=hashlib.sha256).hexdigest()
    return uu+"?"+uu2+"&signature="+signature

def fixx(s,minQty):     #按交易所规则修整下单量
    if s.find(".")==-1:
        return s
    else:
        if minQty=="1":
            return s[:s.find(".")]
        else:
            p=s.find(".")
            p+=len(minQty)-2
            return s[:p+1]

lock=threading.Lock()
API_Key="NfMRIM6hmzZsm3zhU8UPNqtzcCJqczSvqIYT7KBbuf9uqbMHm6JgmwFM3k0qkRku"
Secret_Key="LNoLDg0jeIyBXnX9WJKG6laxClQQ0ggDHPJQp2JVsOeZAWwLaLBL2YQyDAzmLCCh"

#API_Key="fU63fnGR0kmtAnjz38KfdRiCJHnmStwptAYVN4pFIkOCWoSo8OUUEet7WGstxVSV"
#Secret_Key="XQ54JvOpv6QoUXNNMeOH8AwlfGUlwJwMFenRMfOcD3McYwWejEMx72XP11pSau7a"
B_coin_name="USDT"
ab_time=900  #与交易所校对时间的误差，毫秒

if __name__ == "__main__":

    #校对时间并确定1分钟区间--------------
    t=threading.Thread(target=exch_timee)
    t.start()
    t.join(2)
    if t.isAlive ():
        stop_thread(t)
        print("强制结束线程：校对时间  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #print(ab_time)
    #校对时间并确定1分钟区间=============

    all_orderr("BTC")
    print("------------------------")
    #assett()

