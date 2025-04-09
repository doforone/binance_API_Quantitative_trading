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
        print("2")
        with request.urlopen(req, timeout=4) as resp:
            print("3")
            aa=resp.read().decode("utf-8")
            print(aa)
            print("44")
            return aa
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

    
def orderr(symbol,side,type,q_type,quantity):  #下单
    global ddd, USDT
    kk=exch_cc(symbol+"USDT",side,type,q_type,quantity)
    print(kk)
    html=htmll(kk[0],kk[1])
    try:
        temp=json.loads(html)
    except Exception as e:
        print(e)
        temp={}
        
    #print(html)
    if temp!={}:
        if temp["orderId"]>0:
            lock.acquire()
            if side=="BUY":
                ddd["symbols"][symbol]["kline_result"]=0
                ddd["symbols"][symbol]["oth"]=0
                USDT-=ddd["symbols"][symbol]["buy_usdt"]*1.002  #*1.002是考虑手续费的问题
            elif side=="SELL":
                ddd["symbols"][symbol]["kline_result"]=0
                ddd["symbols"][symbol]["buy_price"]=0
                ddd["symbols"][symbol]["sub_price"]=0
                ddd["symbols"][symbol]["oth"]=0
            lock.release()

def exch_cc(symbol,side,type,q_type,quantity):     #下单
    uu="https://api.binance.com/api/v3/order"
    #uu="https://api.binance.com/api/v3/order/test"  #测试下单
    if q_type=="b":  #base如BTC的报价下单
        uu2="symbol="+symbol+"&side="+side+"&type="+type+"&quantity="+quantity+"&recvWindow=5000&timestamp="+str(int(time.time()*1000)-ab_time)
    elif q_type=="q":  #quote如USDT的报价下单
        uu2="symbol="+symbol+"&side="+side+"&type="+type+"&quoteOrderQty="+quantity+"&recvWindow=5000&timestamp="+str(int(time.time()*1000)-ab_time)
                
    signature = hmac.new(Secret_Key.encode(encoding = "utf-8"), uu2.encode(encoding = "utf-8"), digestmod=hashlib.sha256).hexdigest()
    #return uu+"?"+uu2+"&signature="+signature
    return uu,uu2+"&signature="+signature


Secret_Key="XQ54JvOpv6QoUXNNMeOH8AwlfGUlwJwMFenRMfOcD3McYwWejEMx72XP11pSau7a"
API_Key="fU63fnGR0kmtAnjz38KfdRiCJHnmStwptAYVN4pFIkOCWoSo8OUUEet7WGstxVSV"
        
bbb={"1m":60, "3m":180, "5m":300, "15m":900, "30m":1800,
     "1h":3600, "2h":7200, "4h":14400, "6h":21600, "8h":28800, "12h":43200,
     "1d":86400, "3d":259200, "1w":604800}

with open('config.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

USDT=0
balances_id=0
lock=threading.Lock()
run_num=0
ab_time=900  #与交易所校对时间的误差，毫秒
curr_time=0
last_time=0
run=False

if __name__ == "__main__":

    #校对时间并确定间隔区间--------------
    t=threading.Thread(target=exch_timee)
    t.start()
    t.join(3)
    if t.is_alive():
        stop_thread(t)
        print("强制结束线程：校对时间  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    curr_timee=time.time()-ab_time/1000
    if curr_timee%bbb[ddd["interval"]]>=1\
       and curr_timee%bbb[ddd["interval"]]<60\
       and curr_timee//bbb[ddd["interval"]]>last_time//bbb[ddd["interval"]]:  #>=3是为了时间的保守，因为后面要下载K线
        run=True
    #校对时间并确定间隔区间=============


##    t=threading.Thread(
##        target=orderr,args=(
##            "IOTA","SELL","MARKET","b","70.72429"))

    t=threading.Thread(
        target=orderr,args=(
            "IOTA","SELL","MARKET","q","100"))

##    t=threading.Thread(
##        target=orderr,args=(
##            "IOTA","BUY","MARKET","q","100"))
    
    t.setDaemon(True)
    t.start()
    
    print("--end--")
