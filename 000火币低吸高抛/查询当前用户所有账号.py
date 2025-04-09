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
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
                                                     ctypes.py_object(exctype))
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
ab_time=900  #与交易所校对时间的误差，毫秒
api_a="https://"
api_b="api-aws.huobi.pro"
Access_Key="62c8181f-e053099d-e77f3f82-7yngd7gh5g"
Secret_Key="0d4284e9-3b5e706f-0ec4ed17-91c2c"


def htmll(url, params=None, add_to_headers=None):
    headers = {
        "User-Agent": "Chrome",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    if add_to_headers:
        headers.update(add_to_headers)

    postdata=None
    if params:
        postdata = json.dumps(params).encode("utf-8")

    try:
        if postdata:
            req = request.Request(url=url, data=postdata, headers=headers,
                                  origin_req_host=None, unverifiable=False,
                                  method="POST")
        else:
            req = request.Request(url=url, headers=headers,
                                  origin_req_host=None, unverifiable=False,
                                  method="GET")
            
        with request.urlopen(req, timeout=4) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        return ""


def fixx(s,minQty):     #按交易所规则修整下单量
    if s.find(".")==-1:
        return s
    else:
        if str(float(minQty))=="1.0":
            return s[:s.find(".")]
        else:
            p=s.find(".")
            p+=len(str(float(minQty)))-2
            return s[:p+1]


def exch_timee():  #交易所时间
    global ab_time
    uuu=api_a+api_b+"/v1/common/timestamp"
    try:
        html=htmll(uuu)
        ttt=json.loads(html)
        if ttt["status"]=="ok":
            lock.acquire()
            ab_time=int(time.time()*1000)-ttt["data"]
            lock.release()
    except Exception as e:
        #print(e)
        pass


def timee_ab():  #准确UTC时间
    return time.time()-ab_time/1000
    

def huobi_aa():     #查询当前用户的所有账号
    uu="GET\n"+api_b+"\n/v1/account/accounts\n"
    uu2=api_a+api_b+"/v1/account/accounts?"
    
    #时间格式：2017-05-11T16:22:06
    tt=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(timee_ab()-28800))
    tt=quote(tt.encode("utf-8"))
    
    ss=[]
    ss.append("AccessKeyId="+Access_Key)
    ss.append("SignatureMethod=HmacSHA256")
    ss.append("SignatureVersion=2")
    ss.append("Timestamp="+tt)
    ss.sort()
    
    urll="&".join(ss)
    urll2=uu+urll
    signature = hmac.new(
        Secret_Key.encode("utf-8"),
        urll2.encode("utf-8"), digestmod=hashlib.sha256).digest()
    cc=base64.b64encode(signature)
    cc=quote(cc)
    
    return uu2+urll+"&Signature="+cc

def huobi_bb():     #查询指定账户余额
    uu="GET\n"+api_b+"\n/v1/account/accounts/2548899/balance\n"
    uu2=api_a+api_b+"/v1/account/accounts/2548899/balance?"

    #时间格式：2017-05-11T16:22:06
    tt=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(timee_ab()-28800))
    tt=quote(tt.encode("utf-8"))
    
    ss=[]
    ss.append("AccessKeyId="+Access_Key)
    ss.append("SignatureMethod=HmacSHA256")
    ss.append("SignatureVersion=2")
    ss.append("Timestamp="+tt)
    ss.sort()
    
    urll="&".join(ss)
    urll2=uu+urll
    signature = hmac.new(
        Secret_Key.encode("utf-8"), urll2.encode("utf-8"),
        digestmod=hashlib.sha256).digest()
    cc=base64.b64encode(signature)
    cc=quote(cc)
    
    return uu2+urll+"&Signature="+cc


def huobi_bb2():     #获取账户资产估值
    uu="GET\n"+api_b+"\n/v2/account/asset-valuation\n"
    uu2=api_a+api_b+"/v2/account/asset-valuation?"

    #时间格式：2017-05-11T16:22:06
    tt=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(timee_ab()-28800))
    tt=quote(tt.encode("utf-8"))
    
    ss=[]
    ss.append("AccessKeyId="+Access_Key)
    ss.append("SignatureMethod=HmacSHA256")
    ss.append("SignatureVersion=2")
    ss.append("Timestamp="+tt)

    ss.append("accountType=spot")
    ss.append("valuationCurrency=CNY")
    #ss.append("subUid=2548899")
    ss.sort()
    
    urll="&".join(ss)
    urll2=uu+urll
    signature = hmac.new(
        Secret_Key.encode("utf-8"), urll2.encode("utf-8"),
        digestmod=hashlib.sha256).digest()
    cc=base64.b64encode(signature)
    cc=quote(cc)
    
    return uu2+urll+"&Signature="+cc


def huobi_cc(symbol,typee,amountt):  #下单
    uu="POST\n"+api_b+"\n/v1/order/orders/place\n"
    uu2=api_a+api_b+"/v1/order/orders/place?"

    #时间格式：2017-05-11T16:22:06
    tt=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(timee_ab()-28800))
    tt=quote(tt.encode("utf-8"))
    
    ss=[]
    ss.append("AccessKeyId="+Access_Key)
    ss.append("SignatureMethod=HmacSHA256")
    ss.append("SignatureVersion=2")
    ss.append("Timestamp="+tt)
    ss.sort()
    
    urll="&".join(ss)
    urll2=uu+urll
    signature = hmac.new(
        Secret_Key.encode("utf-8"), urll2.encode("utf-8"),
        digestmod=hashlib.sha256).digest()
    cc=base64.b64encode(signature)
    cc=quote(cc)

##    amountt=str(amountt)
##    poss=amountt.find(".")
##    if poss!=-1:
##        amountt=amountt[0:poss+3]

    #dd = parse.urlencode({'account-id': '2548899', 'symbol': 'xmrusdt', 'type': typee, 'amount': amountt})
    dd = {"account-id": 2548899, "amount": amountt, "symbol": symbol,
          "type": typee, "source": "api"}
    #dd=dd.encode('ascii')
    return uu2+urll+"&Signature="+cc, dd


if __name__ == "__main__":
##    kk=huobi_cc("eosusdt","sell-market",2.6066)
##    print(kk)
##    html=htmll(kk[0],kk[1])
##    print(html)

    kk=huobi_bb2()
    html=htmll(kk)
    print(html)

