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
lock=threading.Lock()

def htmll(url, data=None):     #请求页面，这个函数要用线程，长时间不响应就杀死线程，参数5秒有时不起作用
    headers = {}
        
    try:
        if data:
            data=data.encode('utf-8')
        req = request.Request(url, data, headers=headers)
        #resp = request.urlopen(req,timeout=25)
        with request.urlopen(req, timeout=1000) as resp:
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


def K_line(a):  #获取K线数据
    global ddd
    url="https://api.binance.com/api/v3/klines?symbol="+a+"&interval=1h&limit=1000&startTime=1614614400000"
    html=htmll(url)
    try:
        ttt=json.loads(html)
        #ttt["data"].reverse()

        lock.acquire()
        ddd[a]={}
        lock.release()
        
        #id,openn,high,low,closee,amount,vol,count,a_amount,a_vol
        #0  1     2    3   4      5      7   8     9        10

        lock.acquire()
        for tt in ttt:
            ddd[a][int(tt[0]/1000)]={"openn":float(tt[1]), "closee":float(tt[4])}
        lock.release()

    except Exception as e:
        print(a)
        print(e)
        pass


if __name__ == "__main__":
    aaa=['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT',
         'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'TUSDUSDT', 'IOTAUSDT', 'XLMUSDT',
         'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'NULSUSDT', 'VETUSDT',
         'PAXUSDT', 'USDCUSDT', 'LINKUSDT', 'WAVESUSDT', 'BTTUSDT', 'ONGUSDT',
         'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'XMRUSDT',
         'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'DASHUSDT', 'NANOUSDT', 'OMGUSDT',
         'THETAUSDT', 'ENJUSDT', 'MITHUSDT', 'MATICUSDT', 'ATOMUSDT',
         'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT', 'GTOUSDT', 'DOGEUSDT',
         'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'COSUSDT', 'NPXSUSDT', 'COCOSUSDT',
         'MTLUSDT', 'TOMOUSDT', 'PERLUSDT', 'DENTUSDT', 'MFTUSDT', 'KEYUSDT',
         'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT',
         'BUSDUSDT', 'BEAMUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT', 'HBARUSDT',
         'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT', 'RLCUSDT',
         'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'FTTUSDT', 'EURUSDT',
         'OGNUSDT', 'DREPUSDT', 'TCTUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT',
         'BNTUSDT', 'LTOUSDT', 'AIONUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT',
         'WTCUSDT', 'DATAUSDT', 'SOLUSDT', 'CTSIUSDT', 'HIVEUSDT', 'CHRUSDT',
         'GXSUSDT', 'ARDRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'REPUSDT',
         'LRCUSDT', 'PNTUSDT', 'COMPUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT',
         'VTHOUSDT', 'DGBUSDT', 'GBPUSDT', 'SXPUSDT', 'MKRUSDT', 'DCRUSDT',
         'STORJUSDT', 'MANAUSDT', 'AUDUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT',
         'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'SRMUSDT', 'ANTUSDT', 'CRVUSDT',
         'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT',
         'PAXGUSDT', 'WNXMUSDT', 'TRBUSDT', 'BZRXUSDT', 'SUSHIUSDT', 'YFIIUSDT',
         'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT', 'FIOUSDT', 'UMAUSDT',
         'BELUSDT', 'WINGUSDT', 'UNIUSDT', 'NBSUSDT', 'OXTUSDT', 'SUNUSDT',
         'AVAXUSDT', 'HNTUSDT', 'FLMUSDT', 'ORNUSDT', 'UTKUSDT', 'XVSUSDT',
         'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT',
         'CTKUSDT', 'AKROUSDT', 'AXSUSDT', 'HARDUSDT', 'DNTUSDT', 'STRAXUSDT',
         'UNFIUSDT', 'ROSEUSDT', 'AVAUSDT', 'XEMUSDT', 'SKLUSDT', 'SUSDUSDT',
         'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'REEFUSDT', 'OGUSDT',
         'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'RIFUSDT', 'BTCSTUSDT', 'TRUUSDT',
         'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT']
    
    #--去除稳定币
    aaa.remove("AUDUSDT")
    aaa.remove("BUSDUSDT")
    aaa.remove("EURUSDT")
    aaa.remove("GBPUSDT")
    aaa.remove("PAXGUSDT")
    aaa.remove("PAXUSDT")
    aaa.remove("SUSDUSDT")
    aaa.remove("TUSDUSDT")
    aaa.remove("USDCUSDT")
    #=============

    #--去除BNB，因为BNB不小心后台开启折扣25%手续费，会在BNB上扣除手续费，这样下卖单会失败。
    #aaa.remove("BNBUSDT")
    #=============
    aaa.remove("BTCSTUSDT")
    aaa.remove("DREPUSDT")
    aaa.remove("NPXSUSDT")

    ttt={}
    for aa in aaa:
        ttt[aa]=0
        
    ddd={}
    

    for symbol in aaa:
        print(symbol)
        ttt[symbol]=threading.Thread(target=K_line,args=(symbol,))
        ttt[symbol].setDaemon(True)
        ttt[symbol].start()
        have=1
        time.sleep(2)

    #--------------------------------
    if have==1:
        timee_1=time.time()
        alivee=1
        while alivee==1:
            time.sleep(1)
            t_21=time.time()-timee_1
            alivee=0
            for symbol in ttt.keys():
                if ttt[symbol]!=0:
                    if ttt[symbol].is_alive():
                        alivee=1
                        if t_21>1000:
                            stop_thread(ttt[symbol])
                            ttt[symbol]=0
                            print("强制结束线程：K_line  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                            alivee=0
                    else:
                        ttt[symbol]=0
    #==================================

    with open('00所有币种跌幅排行.txt', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(json.dumps(ddd, indent=4)+"\r\n")

    print("--end--")

