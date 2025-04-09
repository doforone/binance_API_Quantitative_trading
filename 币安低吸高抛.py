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

def htmll(url, account="", data=None):     #请求页面，这个函数要用线程，长时间不响应就杀死线程，参数5秒有时不起作用
    if account=="":
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    else:
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36', \
                   'X-MBX-APIKEY': accounts[account]["API_Key"]}
        
    try:
        if data:
            data=data.encode('utf-8')
        req = request.Request(url, data, headers=headers)
        #resp = request.urlopen(req,timeout=25)
        with request.urlopen(req, timeout=4) as resp:
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
    global aa
    url="https://api.binance.com/api/v3/klines?symbol="+a+B_coin_name+"&interval=1m&limit=3"
    html=htmll(url)
    try:
        dd=json.loads(html)
        #dd["data"].reverse()
        dd.pop ()
        lenn_dd=len(dd)
        for ii in range(1,lenn_dd):
            if int(dd[lenn_dd-1][0]/1000)//60==(time.time()-ab_time/1000)//60-1 and float(dd[ii][5])>0 and float(dd[ii-1][5])>0:
                lock.acquire()
                aa[a]["time_id"]=float(dd[ii][0])
                aa[a]["open"]=float(dd[ii][1])
                aa[a]["high"]=float(dd[ii][2])
                aa[a]["low"]=float(dd[ii][3])
                aa[a]["close"]=float(dd[ii][4])
                lock.release()
    except Exception as e:
        print(a)
        print(e)
        pass


def assett(account):  #获取账户各币种余额
    global balances_free
    html=htmll(exch_bb(account),account)
    lock.acquire()
    balances_free["query102"]==1
    try:
        tt=json.loads(html)
        for t in tt["balances"]:
            if float(t["free"])>0 and t["asset"] in aa.keys():
                balances_free[t["asset"]]=float(t["free"])
            elif float(t["free"])>0 and t["asset"]==B_coin_name:
                balances_free[B_coin_name]=float(t["free"])
    except Exception as e:
        print(e)
        pass
    finally:
        lock.release()

def orderr(account,symbol,side,type,q_type,quantity):  #下单
    global tactics, accounts
    kk=exch_cc(account,symbol+B_coin_name,side,type,q_type,quantity)
    print(kk)
    html=htmll(kk[0],account,kk[1])
    try:
        temp=json.loads(html)
    except Exception as e:
        print(e)
        temp={}
        
    #print(html)
    if temp!={}:
        if temp["orderId"]>0:
            lock.acquire()
            accounts[account]["re_config"]=1
            if side=="BUY":
                #tactics[account][symbol]["p"]=tactics[account][symbol]["p"]/(1 + tactics[account][symbol]["per"]*0.01)
                tactics[account][symbol]["p"]=aa[symbol]["close"]
            elif side=="SELL":
                #tactics[account][symbol]["p"]=tactics[account][symbol]["p"]*(1 + tactics[account][symbol]["per"]*0.01)
                tactics[account][symbol]["p"]=aa[symbol]["close"]
            tactics[account][symbol]["time"]=int(time.time()-ab_time/1000)
            lock.release()


def all_orderr(a):  #查询历史订单
    global aa
    kk=exch_dd(a+B_coin_name)
    print(kk)
    html=htmll(kk)
    print(html)
    if html!="":
        try:
            tt=json.loads(html)
            for t in tt:
                if t["side"]=="BUY":
                    lock.acquire()
                    aa[a]["buy_vol"]=float(t["cummulativeQuoteQty"])
                    lock.release()
        except Exception as e:
            pass

def huobi_aa():     #查询当前用户的所有账号
    uu="GET\napi.huobi.pro\n/v1/account/accounts\n"
    uu2="https://api.huobi.pro/v1/account/accounts?"
    tt=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()-28800))   #2017-05-11T16:22:06
    tt=quote(tt.encode("utf-8"))
    ss=[]
    ss.append("AccessKeyId=4901837f-5c5b4vqz6n-644fadbc-5e841")
    ss.append("SignatureMethod=HmacSHA256")
    ss.append("SignatureVersion=2")
    ss.append("Timestamp="+tt)

    ss.sort()
    urll="&".join(ss)
    urll2=uu+urll
    signature = hmac.new(b"24376c57-7f7d16f8-925454db-00b4b", urll2.encode(encoding = "utf-8"), digestmod=hashlib.sha256).digest()
    cc=base64.b64encode(signature)
    cc=quote(cc)
    return uu2+urll+"&Signature="+cc

def exch_bb(account):     #查询指定账户余额
    uu="https://api.binance.com/api/v3/account"
    uu2="recvWindow=5000&timestamp="+str(int(time.time()*1000)-ab_time)
    signature = hmac.new(accounts[account]["Secret_Key"].encode(encoding = "utf-8"), uu2.encode(encoding = "utf-8"), digestmod=hashlib.sha256).hexdigest()
    return uu+"?"+uu2+"&signature="+signature

def exch_cc(account,symbol,side,type,q_type,quantity):     #下单
    uu="https://api.binance.com/api/v3/order"
    if q_type=="b":  #base如BTC的报价下单
        uu2="symbol="+symbol+"&side="+side+"&type="+type+"&quantity="+quantity+"&recvWindow=5000&timestamp="+str(int(time.time()*1000)-ab_time)
    elif q_type=="q":  #quote如USDT的报价下单
        uu2="symbol="+symbol+"&side="+side+"&type="+type+"&quoteOrderQty="+quantity+"&recvWindow=5000&timestamp="+str(int(time.time()*1000)-ab_time)
                
    signature = hmac.new(accounts[account]["Secret_Key"].encode(encoding = "utf-8"), uu2.encode(encoding = "utf-8"), digestmod=hashlib.sha256).hexdigest()
    #return uu+"?"+uu2+"&signature="+signature
    return uu,uu2+"&signature="+signature

def exch_dd(symbol):     #查询历史订单
    uu="https://api.binance.com/api/v3/allOrders"
    uu2="symbol="+symbol+"&limit=1&recvWindow=5000&timestamp="+str(int(time.time()*1000)-ab_time)
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

aa={\
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

#bb={"1m":60, "3m":180, "5m":300, "15m":900, "30m":1800, "1h":3600, "2h":7200, "4h":14400, "6h":21600, "8h":28800, "12h":43200, "1d":86400, "3d":259200, "1w":604800}

B_coin_name="USDT"
lock=threading.Lock()
lock_txt={}
Path="D:\\Python3.8\\bi.kefabu.com\\"
accounts={}
configs=[]
tactics={}  #策略缓存，防止频繁读取文件
balances_free={}
re_config_num=0  #记录没一分钟内account文件中，有多少用户下单了，基价调整了，如果》0则回写account.txt
run_num=0
ab_time=900  #与交易所校对时间的误差，毫秒
last_time=0
run=False

if __name__ == "__main__":
    while True:
        run=False
        re_config_num=0
        try:
            #校对时间并确定1分钟区间--------------
            t=threading.Thread(target=exch_timee)
            t.start()
            t.join(3)
            if t.is_alive():
                stop_thread(t)
                print("强制结束线程：校对时间  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            #print(ab_time)

            timee=time.time()-ab_time/1000
            if timee%60>=3 and timee//60>last_time//60:  #>=2是为了时间的保守，因为后面要下载K线
                run=True
            #校对时间并确定1分钟区间=============

            if run==True:
                #判断lock是否加锁，加锁==1时，证明别的程序正在写入，等待直至0------------
                while True:
                    with open(Path+'lock.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                        lock_txt=json.loads(f.read())
                        if lock_txt["lock"]==1:
                            time.sleep(0.01)
                        else:
                            lock_txt["lock"]=1
                            with open(Path+'lock.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                                f.write(json.dumps(lock_txt, indent=4)+"\r\n")
                            break
                #判断lock是否加锁，加锁==1时，证明别的程序正在写入，等待直至0=============


                #读取account文件-------
                with open(Path+'account.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    accounts=json.loads(f.read())
                #读取account文件=======

                #读取策略参数到内存-----------------------
                for account in accounts.keys():
                    if accounts[account]["on"]==1:   #用户系统开启状态中
                        if run_num==0 or accounts[account]["re_config"]==1:   #防止将来用户量大时少文件读取
                            with open(Path+'config\\'+account+'_a.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                                configs=json.loads(f.read())
                            tactics[account]=configs
                #读取策略参数到内存========================

                #循环检测并下单-----------------------
                for account in tactics.keys():
                    print(account)
                    balances_free={"query102": 0}    #查询现货free余额，键名主要为了防止跟可能的币名重复
                    for symbol in tactics[account].keys():
                        #获取K_line数据------------------------
                        if (time.time()-ab_time/1000)//60>((aa[symbol]["time_id"]/1000)//60)+1:
                            t=threading.Thread(target=K_line,args=(symbol,))
                            t.start()                            
                            t.join(3)
                            if t.is_alive():
                                stop_thread(t)
                                print("强制结束线程K_line  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        #print(aa[symbol])
                        #获取K_line数据========================
                        
                        if (time.time()-ab_time/1000)//60==((aa[symbol]["time_id"]/1000)//60)+1:
                            if aa[symbol]["close"]>tactics[account][symbol]["p"]*(1+tactics[account][symbol]["per"]*0.01):  #没有设=，主要为了防止百分比为0时，开启sell
                                if balances_free["query102"]==0:
                                    #查询账户余额--------------
                                    t=threading.Thread(target=assett,args=(account,))
                                    t.start()
                                    t.join(3)
                                    if t.is_alive():
                                        stop_thread(t)
                                        print("强制结束线程:查询账户余额！......"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                                    #查询账户余额==============

                                if symbol in balances_free.keys():
                                    if tactics[account][symbol]["q_type"]=="b":  #base基础币报价如：BTC
                                        if (balances_free[symbol]>=tactics[account][symbol]["q"]
                                            and tactics[account][symbol]["q"]<=float(aa[symbol]["maxQty"])
                                            and tactics[account][symbol]["q"]>=float(aa[symbol]["minQty"])):
                                            #----------下sell单=q
                                            tactics[account][symbol]["oth"]=threading.Thread(target=orderr,args=(account,symbol,"SELL","MARKET","b",fixx(str(tactics[account][symbol]["q"]),aa[symbol]["minQty"])))
                                            tactics[account][symbol]["oth"].setDaemon(True)
                                            tactics[account][symbol]["oth"].start()

                                        elif (balances_free[symbol]<tactics[account][symbol]["q"]
                                              and balances_free[symbol]<=float(aa[symbol]["maxQty"])
                                              and balances_free[symbol]>=float(aa[symbol]["minQty"])):
                                            #----------下sell单<q
                                            tactics[account][symbol]["oth"]=threading.Thread(target=orderr,args=(account,symbol,"SELL","MARKET","b",fixx(str(balances_free[symbol]),aa[symbol]["minQty"])))
                                            tactics[account][symbol]["oth"].setDaemon(True)
                                            tactics[account][symbol]["oth"].start()
                                    elif tactics[account][symbol]["q_type"]=="q": #quote报价币：USDT
                                        if tactics[account][symbol]["q"]>=10:
                                            #----------下sell单=q，即可
                                            tactics[account][symbol]["oth"]=threading.Thread(target=orderr,args=(account,symbol,"SELL","MARKET","q",fixx(str(tactics[account][symbol]["q"]),"0.01")))
                                            tactics[account][symbol]["oth"].setDaemon(True)
                                            tactics[account][symbol]["oth"].start()
                                    
                            elif (aa[symbol]["close"]<tactics[account][symbol]["p"]/(1+tactics[account][symbol]["per"]*0.01)
                                  and int((aa[symbol]["time_id"]/1000+60)%tactics[account][symbol]["again"])==0):  #没有设=，主要为了防止百分比为0时，开启buy
                                if balances_free["query102"]==0:
                                    #查询账户余额--------------
                                    t=threading.Thread(target=assett,args=(account,))
                                    t.start()
                                    t.join(3)
                                    if t.is_alive():
                                        stop_thread(t)
                                        print("强制结束线程:查询账户余额！......"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                                    #查询账户余额==============
                                        
                                if B_coin_name in balances_free.keys():
                                    if tactics[account][symbol]["q_type"]=="b":  #base基础币报价如：BTC
                                        if (tactics[account][symbol]["q"]<=float(aa[symbol]["maxQty"])
                                            and tactics[account][symbol]["q"]>=float(aa[symbol]["minQty"])
                                            and balances_free[B_coin_name]>tactics[account][symbol]["q"]*aa[symbol]["close"]*1.1):
                                            #----------下buy单=q
                                            tactics[account][symbol]["oth"]=threading.Thread(target=orderr,args=(account,symbol,"BUY","MARKET","b",fixx(str(tactics[account][symbol]["q"]),aa[symbol]["minQty"])))
                                            tactics[account][symbol]["oth"].setDaemon(True)
                                            tactics[account][symbol]["oth"].start()
                                        elif (tactics[account][symbol]["q"]<=float(aa[symbol]["maxQty"])
                                            and tactics[account][symbol]["q"]>=float(aa[symbol]["minQty"])
                                            and balances_free[B_coin_name]<=tactics[account][symbol]["q"]*aa[symbol]["close"]*1.1):
                                            #----------下buy单  q类型
                                            tactics[account][symbol]["oth"]=threading.Thread(target=orderr,args=(account,symbol,"BUY","MARKET","q",fixx(str(balances_free[B_coin_name]),"0.01")))
                                            tactics[account][symbol]["oth"].setDaemon(True)
                                            tactics[account][symbol]["oth"].start()
                                    elif tactics[account][symbol]["q_type"]=="q":  #quote报价币：USDT
##                                        if tactics[account][symbol]["q"]>=10 and balances_free[B_coin_name]>=tactics[account][symbol]["q"]:
##                                            #----------下buy单=q
##                                            tactics[account][symbol]["oth"]=threading.Thread(target=orderr,args=(account,symbol+B_coin_name,"BUY","MARKET",q_type,fixx(str(tactics[account][symbol]["q"]),"0.01")))
##                                            tactics[account][symbol]["oth"].setDaemon(True)
##                                            tactics[account][symbol]["oth"].start()
##                                        elif balances_free[B_coin_name]>=10 and balances_free[B_coin_name]<tactics[account][symbol]["q"]:
##                                            #----------下buy单<q
##                                            tactics[account][symbol]["oth"]=threading.Thread(target=orderr,args=(account,symbol+B_coin_name,"BUY","MARKET",q_type,fixx(str(balances_free[B_coin_name]),"0.01")))
##                                            tactics[account][symbol]["oth"].setDaemon(True)
##                                            tactics[account][symbol]["oth"].start()
                                        if tactics[account][symbol]["q"]>=10 and balances_free[B_coin_name]>=10:
                                            #----------下buy单=q
                                            tactics[account][symbol]["oth"]=threading.Thread(target=orderr,args=(account,symbol,"BUY","MARKET","q",fixx(str(tactics[account][symbol]["q"]),"0.01")))
                                            tactics[account][symbol]["oth"].setDaemon(True)
                                            tactics[account][symbol]["oth"].start()
                                            
                #--------------------------------
                timee_1=time.time()
                alivee=1
                while alivee==1:
                    time.sleep(1)
                    t_21=time.time()-timee_1
                    alivee=0
                    for account in tactics.keys():
                        for symbol in tactics[account].keys():
                            if tactics[account][symbol]['oth']!=0:
                                if tactics[account][symbol]['oth'].is_alive():
                                    alivee=1
                                    if t_21>3:
                                        stop_thread(tactics[account][symbol]['oth'])
                                        tactics[account][symbol]['oth']=0
                                        print("强制结束线程：下单  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                                        alivee=0
                                else:
                                    tactics[account][symbol]['oth']=0

                #循环检测并下单=======================

                #re_config设置为0，并回写文件---------------
                for account in accounts.keys():
                    if accounts[account]["re_config"]==1:
                        if account in tactics.keys():
                            with open(Path+'config\\'+account+'_a.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                                f.write(json.dumps(tactics[account], indent=4)+"\r\n")
                        accounts[account]["re_config"]=0
                        re_config_num+=1

                if re_config_num>0:
                    with open(Path+'account.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                        f.write(json.dumps(accounts, indent=4)+"\r\n")
                #re_config设置为0，并回写文件===============

                #解锁-------------------
                lock_txt["lock"]=0
                with open(Path+'lock.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(lock_txt, indent=4)+"\r\n")
                #解锁===================

                #设定已经第一次运行过，和上次运行时间-------------------
                run_num+=1
                last_time=time.time()-ab_time/1000
                #设定已经第一次运行过，和上次运行时间===================
                
        except Exception as e:  #防止死锁
            lock_txt["lock"]=0
            with open(Path+'lock.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                f.write(json.dumps(lock_txt, indent=4)+"\r\n")
            print(e)


        print(str(run_num)+"  币安后台自动交易")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        time.sleep(1)
        pass
        time.sleep(1)
