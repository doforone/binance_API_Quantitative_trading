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

    ccc={"1.00000000":"1.0", "0.10000000":"0.1", "0.01000000":"0.01", "0.00100000":"0.001",
         "0.00010000":"0.0001", "0.00001000":"0.00001", "0.00000100":"0.000001",
         "0.00000010":"0.0000001", "0.00000001":"0.00000001"}
    
    config={"interval": "1h",
            "AA": 4,
            "VV": 4,
            "AB": 1,
            "MN": 97,
            "symbols": {}
            }

    with open('币安所有参数.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ttt=json.loads(f.read())

    for symbol in ttt["symbols"]:
        if symbol["symbol"] in aaa and symbol["status"]=="TRADING" and "MARKET" in symbol["orderTypes"]:
            config["symbols"][symbol["baseAsset"]]={}
            config["symbols"][symbol["baseAsset"]]["minQty"]=ccc[symbol["filters"][2]["minQty"]]
            config["symbols"][symbol["baseAsset"]]["minNotional"]=symbol["filters"][3]["minNotional"]
            config["symbols"][symbol["baseAsset"]]["maxQty"]=symbol["filters"][5]["maxQty"]
            
            config["symbols"][symbol["baseAsset"]]["buy_usdt"]=120

            config["symbols"][symbol["baseAsset"]]["balances"]="0"
            config["symbols"][symbol["baseAsset"]]["kline_id"]=0
            config["symbols"][symbol["baseAsset"]]["kline_result"]=0
            config["symbols"][symbol["baseAsset"]]["buy_price"]=0
            config["symbols"][symbol["baseAsset"]]["sub_price"]=0

            config["symbols"][symbol["baseAsset"]]["oth"]=0

            if symbol["filters"][2]["minQty"]!=symbol["filters"][2]["stepSize"]:
                print(symbol["symbol"])

    with open('config2.txt', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(json.dumps(config, indent=4)+"\r\n")

