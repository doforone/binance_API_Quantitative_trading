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
            
        with request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(e)
        return ""


def fixx(s,minQty):     #按交易所规则修整下单量
    if s.find(".")==-1:
        return s
    else:
        if minQty=="1.0":
            return s[:s.find(".")]
        else:
            p=s.find(".")
            p+=len(minQty)-2
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
    

def huobi_aa():  #查询当前用户的所有账号
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
        Secret_Key.encode("utf-8"), urll2.encode("utf-8"),
        digestmod=hashlib.sha256).digest()
    cc=base64.b64encode(signature)
    cc=quote(cc)
    
    return uu2+urll+"&Signature="+cc


def huobi_bb():  #查询指定账户余额
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


def huobi_bb2():  #获取账户资产估值
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


def huobi_cc(symbol,typee,amountt):  #下单，火币buy单不小于5usdt
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


def assett():  #获取账户各币种余额
    global ddd, USDT, balances_id
    kk=huobi_bb()
    try:
        html=htmll(kk)
        ttt=json.loads(html)
        if ttt["status"]=="ok":
            lock.acquire()
            for tt in ttt["data"]["list"]:
                if float(tt["balance"])>0 and tt["currency"] in ddd["symbols"].keys()\
                   and tt["type"]=="trade":
                    ddd["symbols"][tt["currency"]]["balances"]=tt["balance"]
                elif float(tt["balance"])>0 and tt["currency"]=="usdt"\
                     and tt["type"]=="trade":
                    USDT=float(tt["balance"])
                    print(USDT)
            balances_id=timee_ab()
            lock.release()
    except Exception as e:
        print(e)
        pass
    finally:
        pass

        
def orderr(symbol,typee,amountt):  #下单
    global ddd, USDT
    kk=huobi_cc(symbol+"usdt",typee,amountt)
    try:
        html=htmll(kk[0],kk[1])
        ttt=json.loads(html)
        if ttt["status"]=="ok":
            print(kk[1])
            lock.acquire()
            if typee=="buy-market":
                ddd["symbols"][symbol]["kline_result"]=0
                ddd["symbols"][symbol]["oth"]=0
                USDT-=ddd["symbols"][symbol]["buy_usdt"]*1.002  #*1.002是考虑手续费的问题
            elif typee=="sell-market":
                ddd["symbols"][symbol]["kline_result"]=0
                ddd["symbols"][symbol]["buy_price"]=0
                ddd["symbols"][symbol]["sub_price"]=0
                ddd["symbols"][symbol]["oth"]=0
            lock.release()
    except Exception as e:
        print(e)


def K_line(a):  #获取K线数据
    global ddd
    mmm_nnn=[]
    url=api_a+api_b+"/market/history/kline?period="+ddd[
        "interval"]+"&size="+str(ddd["MN"]+1)+"&symbol="+a+"usdt"

    try:
        html=htmll(url)
        ttt=json.loads(html)
        if ttt["status"]=="ok":
            ttt["data"].reverse()  #改成时间从小到大排序

            lock.acquire()
            ddd["symbols"][a]["kline_id"]=time.time()
            lock.release()

            if ttt["data"][-1]["id"]//bbb[ddd["interval"]]==timee_ab()//bbb[
                ddd["interval"]]:
                ttt["data"].pop()
            else:
                print(f"{a}: 不正常----")

            if ttt["data"][-1]["id"]//bbb[ddd["interval"]]==timee_ab()//bbb[
                ddd["interval"]]-1:
                #id  amount  count  open  close  low  high  vol

                for tt in ttt["data"]:
                    mmm_nnn.append(tt["close"]-tt["open"])

                #计算是否买入
                if float(ddd["symbols"][a]["balances"])<ddd["symbols"][a][
                    "sell-market-min-order-amt"]:
                    if mmm_nnn[-1]<-max(mmm_nnn[:-1])*ddd["AB"]\
                       and mmm_nnn[-1]<min(mmm_nnn[:-1])*ddd["AB"] and mmm_nnn[-2]<0:
                        lock.acquire()
                        ddd["symbols"][a]["kline_result"]=1  #买入
                        ddd["symbols"][a]["buy_price"]=ttt["data"][-1]["close"]
                        ddd["symbols"][a]["sub_price"]=abs(mmm_nnn[-1])
                        lock.release()
                else:
##                    if ttt["data"][-1]["close"]>ddd[
##                        "symbols"][a]["buy_price"]+ddd[
##                            "AA"]*ddd["symbols"][a]["sub_price"]\
##                       or ttt["data"][-1]["close"]<ddd[
##                           "symbols"][a]["buy_price"]-ddd[
##                               "VV"]*ddd["symbols"][a]["sub_price"]:
                    if mmm_nnn[-1]>max(mmm_nnn[:-1])*ddd["AB"] and mmm_nnn[-1]>-min(mmm_nnn[:-1])*ddd["AB"]:
                        lock.acquire()
                        ddd["symbols"][a]["kline_result"]=-1  #卖出
                        lock.release()
        else:
            print(f"{a}: 2不正常====")

    except Exception as e:
        print(a)
        print(e)
        pass


with open('config.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
    ddd=json.loads(f.read())

ab_time=900  #与交易所校对时间的误差，毫秒
api_a="https://"
api_b="api-aws.huobi.pro"
Access_Key="62c8181f-e053099d-e77f3f82-7yngd7gh5g"
Secret_Key="0d4284e9-3b5e706f-0ec4ed17-91c2c"
bbb={"5min":300, "15min":900, "30min":1800, "60min":3600,
     "4hour":14400, "1day":86400}
USDT=0
balances_id=0
lock=threading.Lock()
run_num=0
curr_time=0
last_time=0
run=False


if __name__ == "__main__":
    while True:
        run=False
        try:
            #读取all_sell文件-------
            with open('all_sell.txt', 'r', encoding='utf-8-sig',
                      newline='\r\n') as f:
                ttt=json.loads(f.read())
            #读取account文件=======
            
            #校对时间并确定间隔区间--------------
            t=threading.Thread(target=exch_timee)
            t.start()
            t.join(5)
            if t.is_alive():
                stop_thread(t)
                print("强制结束线程：校对时间  "+time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime()))

            #>=15是为了时间的保守，因为有些小币种K线生成太慢
            curr_timee=timee_ab()
            if ttt["all_sell"]==1 or (curr_timee%bbb[ddd["interval"]]>=6\
               and curr_timee%bbb[ddd["interval"]]<120\
               and curr_timee//bbb[ddd["interval"]]>last_time//bbb[
                   ddd["interval"]]):
                run=True
            #校对时间并确定间隔区间=============

            if run==True:
                #读取config文件-------
                with open('config.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    ddd=json.loads(f.read())
                #读取account文件=======

                #查询账户余额--------------
                for symbol in ddd["symbols"].keys():
                    ddd["symbols"][symbol]["balances"]="0"
                    ddd["symbols"][symbol]["kline_result"]=0  #重置，因为可能有上次没有执行的买单，由于USDT不够
                
                balances_id=0
                numm=0
                while curr_timee//bbb[ddd["interval"]]>balances_id//bbb[ddd["interval"]] and numm<4:
                    t=threading.Thread(target=assett)
                    t.start()
                    t.join(5)
                    if t.is_alive():
                        stop_thread(t)
                        print("强制结束线程:查询账户余额！......"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    numm+=1
                    time.sleep(0.1)
                #查询账户余额==============


                #获取K_line数据------------------------
                have=1
                numm=0
                while have==1 and numm<4:
                    have=0
                    for symbol in ddd["symbols"].keys():
                        if curr_timee//bbb[ddd["interval"]]>ddd["symbols"][symbol]["kline_id"]//bbb[ddd["interval"]]:
                            ddd["symbols"][symbol]["oth"]=threading.Thread(target=K_line,args=(symbol,))
                            ddd["symbols"][symbol]["oth"].setDaemon(True)
                            ddd["symbols"][symbol]["oth"].start()
                            have=1

                    #--------------------------------
                    if have==1:
                        timee_1=time.time()
                        alivee=1
                        while alivee==1:
                            time.sleep(1)
                            t_21=time.time()-timee_1
                            alivee=0
                            for symbol in ddd["symbols"].keys():
                                if ddd["symbols"][symbol]['oth']!=0:
                                    if ddd["symbols"][symbol]['oth'].is_alive():
                                        alivee=1
                                        if t_21>10:
                                            stop_thread(ddd["symbols"][symbol]['oth'])
                                            ddd["symbols"][symbol]['oth']=0
                                            print("强制结束线程：K_line  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                                            alivee=0
                                    else:
                                        ddd["symbols"][symbol]['oth']=0
                    #==================================
                    numm+=1
                    time.sleep(0.1)
                #获取K_line数据========================


                #先执行卖单，回笼资金------------------------
                have=1
                numm=0
                while have==1 and numm<4:
                    have=0
                    for symbol in ddd["symbols"].keys():
                        if ddd["symbols"][symbol]["kline_result"]==-1:
                            ddd["symbols"][symbol]["oth"]=threading.Thread(
                                target=orderr,args=(
                                    symbol,"sell-market",fixx(
                                        ddd["symbols"][symbol]["balances"],ddd["symbols"][symbol]["amount-precision"])))
                            
                            ddd["symbols"][symbol]["oth"].setDaemon(True)
                            ddd["symbols"][symbol]["oth"].start()
                            have=1

                    #--------------------------------
                    if have==1:
                        timee_1=time.time()
                        alivee=1
                        while alivee==1:
                            time.sleep(1)
                            t_21=time.time()-timee_1
                            alivee=0
                            for symbol in ddd["symbols"].keys():
                                if ddd["symbols"][symbol]['oth']!=0:
                                    if ddd["symbols"][symbol]['oth'].is_alive():
                                        alivee=1
                                        if t_21>10:
                                            stop_thread(ddd["symbols"][symbol]['oth'])
                                            ddd["symbols"][symbol]['oth']=0
                                            print("强制结束线程：K_line  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                                            alivee=0
                                    else:
                                        ddd["symbols"][symbol]['oth']=0
                    #==================================

                    #查询账户余额--------------
                    for symbol in ddd["symbols"].keys():
                        ddd["symbols"][symbol]["balances"]="0"
                    
                    balances_id=0
                    numm2=0
                    while curr_timee//bbb[ddd["interval"]]>balances_id//bbb[ddd["interval"]] and numm2<4:
                        t=threading.Thread(target=assett)
                        t.start()
                        t.join(5)
                        if t.is_alive():
                            stop_thread(t)
                            print("强制结束线程:查询账户余额！......"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        numm2+=1
                        time.sleep(0.1)
                    #查询账户余额==============
                    numm+=1
                    time.sleep(0.1)
                #先执行卖单，回笼资金========================


##                #查询账户余额--------------
##                balances_id=0
##                while curr_timee//bbb[ddd["interval"]]>balances_id//bbb[ddd["interval"]]:
##                    t=threading.Thread(target=assett)
##                    t.start()
##                    t.join(3)
##                    if t.is_alive():
##                        stop_thread(t)
##                        print("强制结束线程:查询账户余额！......"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
##                #查询账户余额==============


                #执行买单------------------------因为更新usdt，所以买单要串行计算
                have=1
                numm=0
                while have==1 and ttt["all_sell"]==0 and numm<4:  #全部卖出的时候，就不再买入了
                    have=0
                    for symbol in ddd["symbols"].keys():
                        if ddd["symbols"][symbol]["kline_result"]==1\
                           and USDT>ddd["symbols"][symbol]["buy_usdt"]*1.002:  #*1.002是考虑手续费的问题
                            ddd["symbols"][symbol]["oth"]=threading.Thread(
                                target=orderr,args=(
                                    symbol,"buy-market",fixx(
                                        str(ddd["symbols"][symbol]["buy_usdt"]),"0.01")))
                            
                            ddd["symbols"][symbol]["oth"].setDaemon(True)
                            ddd["symbols"][symbol]["oth"].start()
                            ddd["symbols"][symbol]["oth"].join(5)  #串行计算
                            have=1

                    #查询账户余额--------------
                    for symbol in ddd["symbols"].keys():
                        ddd["symbols"][symbol]["balances"]="0"
                        ddd["symbols"][symbol]["oth"]=0  #很重要，防止后面的回写出错
                        
                    balances_id=0
                    numm2=0
                    while curr_timee//bbb[ddd["interval"]]>balances_id//bbb[ddd["interval"]] and numm2<4:
                        t=threading.Thread(target=assett)
                        t.start()
                        t.join(5)
                        if t.is_alive():
                            stop_thread(t)
                            print("强制结束线程:查询账户余额！......"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        numm2+=1
                        time.sleep(0.1)
                    #查询账户余额==============

                    numm+=1
                    time.sleep(0.1)
##                    #--------------------------------
##                    if have==1:
##                        timee_1=time.time()
##                        alivee=1
##                        while alivee==1:
##                            time.sleep(1)
##                            t_21=time.time()-timee_1
##                            alivee=0
##                            for symbol in ddd["symbols"].keys():
##                                if ddd["symbols"][symbol]['oth']!=0:
##                                    if ddd["symbols"][symbol]['oth'].is_alive():
##                                        alivee=1
##                                        if t_21>5:
##                                            stop_thread(ddd["symbols"][symbol]['oth'])
##                                            ddd["symbols"][symbol]['oth']=0
##                                            print("强制结束线程：K_line  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
##                                            alivee=0
##                                    else:
##                                        ddd["symbols"][symbol]['oth']=0
##                    #==================================
                #执行买单==============================


                #回写文件---------------
                if ttt["all_sell"]==1:
                    ttt["all_sell"]=0
                    with open('all_sell.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                        f.write(json.dumps(ttt, indent=4)+"\r\n")

                try:
                    jjj=json.dumps(ddd, indent=4)+"\r\n"
                    with open('config.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                        f.write(jjj)
                except Exception as ee:
                    print(ee)
                    print("--回写config出错--")
                #回写文件===============


                #设定已经第一次运行过，和上次运行时间-------------------
                run_num+=1
                last_time=time.time()-ab_time/1000
                print(str(run_num)+"  火币000低吸高抛_3版")
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                #设定已经第一次运行过，和上次运行时间===================
                
        except Exception as e:  #防止死锁
            print(e)

        time.sleep(2)
