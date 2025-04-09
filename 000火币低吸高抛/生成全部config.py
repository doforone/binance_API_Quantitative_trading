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
    aaa=['btcusdt', 'ethusdt', 'eosusdt', 'bchusdt', 'xrpusdt', 'ltcusdt',
         'htusdt', 'bsvusdt', 'trxusdt', 'linkusdt', 'dotusdt', 'adausdt',
         'jstusdt', 'etcusdt', 'bttusdt', 'zecusdt', 'uniusdt', 'dogeusdt',
         'dashusdt', 'filusdt', 'omgusdt', 'sunusdt', 'sushiusdt', 'iostusdt',
         'ontusdt', 'xlmusdt', 'atomusdt', 'seeleusdt', 'qtumusdt', 'mdxusdt',
         'yfiusdt', 'neousdt', 'crvusdt', 'yfiiusdt', 'xmrusdt', 'grtusdt',
         'thetausdt', 'algousdt', 'zilusdt', 'aaveusdt', 'btmusdt', 'bagsusdt',
         'xtzusdt', 'aacusdt', 'wiccusdt', 'crousdt', 'lambusdt', 'hcusdt',
         'ttusdt', 'zksusdt', 'vetusdt', '1inchusdt', 'dacusdt', 'rsrusdt',
         'nodeusdt', 'newusdt', 'lunausdt', 'achusdt', 'ksmusdt', 'iotausdt',
         'elfusdt', 'topusdt', 'kavausdt', 'xemusdt', 'zrxusdt', 'elausdt',
         'akrousdt', 'nasusdt', 'renusdt', 'cvcusdt', 'hptusdt', 'ctxcusdt',
         'nearusdt', 'storjusdt', 'flowusdt', 'gxcusdt', 'actusdt', 'phausdt',
         'letusdt', 'bandusdt', 'maticusdt', 'polsusdt', 'socusdt', 'mxusdt',
         'paiusdt', 'btsusdt', 'itcusdt', 'dtausdt', 'badgerusdt', 'antusdt',
         'snxusdt', 'maskusdt', 'compusdt', 'ruffusdt', 'sntusdt', 'nestusdt',
         'wavesusdt', 'kcashusdt', 'hiveusdt', 'titanusdt',
         'chzusdt', 'forusdt', 'gofusdt', 'ogousdt', 'avaxusdt', 'glmusdt',
         'egtusdt', 'valueusdt', 'ektusdt', 'manausdt', 'reefusdt',
         'steemusdt', 'mdsusdt', 'irisusdt', 'aeusdt', 'trbusdt', 'emusdt',
         'batusdt', 'pearlusdt', 'ckbusdt', 'bhdusdt', 'nulsusdt', 'smtusdt',
         'cmtusdt', 'nexousdt', 'massusdt', 'fsnusdt', 'ocnusdt', 'woousdt',
         'fttusdt', 'arpausdt', 'zenusdt', 'lbausdt', 'chrusdt', 'pondusdt',
         'lrcusdt', 'mkrusdt', 'vsysusdt', 'solusdt', 'hbcusdt', 'mxcusdt',
         'borusdt', 'skmusdt', 'vidyusdt', 'sandusdt', 'bixusdt', 'swrvusdt',
         'balusdt', 'atpusdt', 'iotxusdt', 'wtcusdt', 'wnxmusdt', 'gtusdt',
         'sklusdt', 'lxtusdt', 'frontusdt', 'nknusdt', 'ognusdt', 'kncusdt',
         'uuuusdt', 'lolusdt', 'rvnusdt', 'umausdt', 'arusdt', 'nbsusdt',
         'ankrusdt', 'oneusdt', 'oxtusdt', 'nanousdt', 'xrtusdt', 'uipusdt',
         'dcrusdt', 'kanusdt', 'cruusdt', 'bntusdt', 'pvtusdt', 'dkausdt',
         'firousdt', 'icxusdt', 'fisusdt', 'mtausdt', 'creusdt', 'astusdt',
         'bchausdt', 'linausdt', 'loomusdt', 'blzusdt', 'dfusdt', 'dockusdt',
         'cnnsusdt', 'hitusdt', 'auctionusdt', 'ringusdt', 'api3usdt',
         'yamusdt', 'hotusdt', 'wxtusdt', 'gnxusdt', 'waxpusdt', 'yeeusdt',
         'injusdt', 'hbarusdt', 'swftcusdt', 'nhbtcusdt', 'ftiusdt', 'cvpusdt',
         'nsureusdt', 'dhtusdt', 'abtusdt', 'mlnusdt', 'xmxusdt', 'utkusdt',
         'bethusdt', 'tnbusdt', 'stptusdt']
    
    #已去除稳定币dai, pax, usdc，还有hb10

    config={"interval": "60min",
            "AA": 4,
            "VV": 4,
            "AB": 1,
            "MN": 97,
            "symbols": {}
            }

    ccc={0:"1.0",1:"0.1",2:"0.01",3:"0.001",4:"0.0001",5:"0.00001",6:"0.000001",
         7:"0.0000001",8:"0.00000001"}

    with open('火币交易对.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ddd=json.loads(f.read())

    for aa in aaa[:]:
        for dd in ddd["data"]:
            if dd["symbol"]==aa:
                config["symbols"][dd["base-currency"]]={}
                config["symbols"][dd["base-currency"]][
                    "amount-precision"]=ccc[dd["amount-precision"]]
                config["symbols"][dd["base-currency"]][
                    "sell-market-min-order-amt"]=dd["sell-market-min-order-amt"]
            
                config["symbols"][dd["base-currency"]]["buy_usdt"]=80

                config["symbols"][dd["base-currency"]]["balances"]="0"
                config["symbols"][dd["base-currency"]]["kline_id"]=0
                config["symbols"][dd["base-currency"]]["kline_result"]=0
                config["symbols"][dd["base-currency"]]["buy_price"]=0
                config["symbols"][dd["base-currency"]]["sub_price"]=0

                config["symbols"][dd["base-currency"]]["oth"]=0

                break


    with open('config2.txt', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(json.dumps(config, indent=4)+"\r\n")

