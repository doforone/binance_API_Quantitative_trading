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

aaa={\
     'BTC': {'minQty': '0.000001', 'minNotional': '10', 'maxQty': '574.95143224', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ETH': {'minQty': '0.00001', 'minNotional': '10', 'maxQty': '9000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'BNB': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '80773.11635675', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'NEO': {'minQty': '0.001', 'minNotional': '10', 'maxQty': '198142.67851722', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'LTC': {'minQty': '0.00001', 'minNotional': '10', 'maxQty': '69692.75786125', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'QTUM': {'minQty': '0.001', 'minNotional': '10', 'maxQty': '173711.32441667', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ADA': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'XRP': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'EOS': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '576594.41922176', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'IOTA': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '900000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'XLM': {'minQty': '0.1', 'minNotional': '0.1', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ONT': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '827908.03147383', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'TRX': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ETC': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '186716.20576446', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ICX': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '900000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'NULS': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '326394.46650826', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'VET': {'minQty': '1', 'minNotional': '10', 'maxQty': '90000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'BCH': {'minQty': '0.00001', 'minNotional': '10', 'maxQty': '11111.79284258', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'LINK': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '758214.98137052', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'WAVES': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '184731.81643251', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'BTT': {'minQty': '1', 'minNotional': '10', 'maxQty': '90000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ONG': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '437369.29491047', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'HOT': {'minQty': '1', 'minNotional': '10', 'maxQty': '90000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ZIL': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ZRX': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '794111.23714876', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'FET': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '6976462.61356749', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'BAT': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '900000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'XMR': {'minQty': '0.00001', 'minNotional': '10', 'maxQty': '8476.27747728', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ZEC': {'minQty': '0.00001', 'minNotional': '10', 'maxQty': '24860.98598241', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'IOST': {'minQty': '1', 'minNotional': '10', 'maxQty': '48391252.69421488', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'CELR': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'DASH': {'minQty': '0.00001', 'minNotional': '10', 'maxQty': '15041.46253521', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'NANO': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '253001.71944904', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'OMG': {'minQty': '0.01', 'minNotional': '10', 'maxQty': '172905.51408402', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'THETA': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '1912811.24786501', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ENJ': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '1828250.00530303', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'MITH': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'MATIC': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ATOM': {'minQty': '0.001', 'minNotional': '10', 'maxQty': '280132.1260978', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'TFUEL': {'minQty': '1', 'minNotional': '10', 'maxQty': '26628429.77892562', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'ONE': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0},\
     'FTM': {'minQty': '0.1', 'minNotional': '10', 'maxQty': '9000000', "time_id": 0, "open": 0, "close": 0, "high": 0, "low": 0}\
     }

config={"interval": "1h", \
        "AA": 6, \
        "VV": 6, \
        "AB": 1, \
        "MN": 97, \
	"symbols": {}\
        }

if __name__ == "__main__" and 1==1:
    for aa in aaa.keys():
        config["symbols"][aa]={}
        config["symbols"][aa]["minQty"]=aaa[aa]["minQty"]
        config["symbols"][aa]["minNotional"]=aaa[aa]["minNotional"]
        config["symbols"][aa]["maxQty"]=aaa[aa]["maxQty"]
        
        config["symbols"][aa]["buy_usdt"]=100

        config["symbols"][aa]["balances"]=0
        config["symbols"][aa]["kline_id"]=0
        config["symbols"][aa]["kline_result"]=0
        config["symbols"][aa]["buy_price"]=0
        config["symbols"][aa]["sub_price"]=0

        config["symbols"][aa]["oth"]=0

    with open('config.txt', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(json.dumps(config, indent=4)+"\r\n")

    print("重新设置完毕。")
