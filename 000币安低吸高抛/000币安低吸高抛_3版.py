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
        with request.urlopen(req, timeout=10) as resp:
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
    mmm_nnn=[]
    url="https://api.binance.com/api/v3/klines?symbol="+a+"USDT"+"&interval="+ddd["interval"]+"&limit="+str(ddd["MN"]+1)
    html=htmll(url)
    try:
        ttt=json.loads(html)
        #ttt["data"].reverse()

        lock.acquire()
        ddd["symbols"][a]["kline_id"]=time.time()
        lock.release()
        
        if (ttt[-1][0]/1000)//bbb[ddd["interval"]]==(time.time()-ab_time/1000)//bbb[ddd["interval"]]:
            ttt.pop()
        else:
            print(f"{a}: 不正常----")

        if (ttt[-1][0]/1000)//bbb[ddd["interval"]]==(time.time()-ab_time/1000)//bbb[ddd["interval"]]-1:
            #id,openn,high,low,closee,amount,vol,count,a_amount,a_vol
            #0  1     2    3   4      5      7   8     9        10

            for tt in ttt:
                mmm_nnn.append(float(tt[4])-float(tt[1]))

            #if ddd["symbols"][a]["buy_price"]==0:  #计算是否买入
            if float(ddd["symbols"][a]["balances"])*float(ttt[-1][4])<=20:  #计算是否买入
                if mmm_nnn[-1]<-max(mmm_nnn[:-1])*ddd["AB"] and mmm_nnn[-1]<min(mmm_nnn[:-1])*ddd["AB"] and mmm_nnn[-2]<0:
                    lock.acquire()
                    ddd["symbols"][a]["kline_result"]=1  #买入
                    ddd["symbols"][a]["buy_price"]=float(ttt[-1][4])
                    ddd["symbols"][a]["sub_price"]=abs(mmm_nnn[-1])
                    lock.release()
            else:
##                if (float(ttt[-1][4])>ddd["symbols"][a]["buy_price"]+ddd["AA"]*ddd["symbols"][a]["sub_price"]\
##                   or float(ttt[-1][4])<ddd["symbols"][a]["buy_price"]-ddd["VV"]*ddd["symbols"][a]["sub_price"])\
##                   and float(ddd["symbols"][a]["balances"])*float(ttt[-1][4])>20:
                if (mmm_nnn[-1]>max(mmm_nnn[:-1])*ddd["AB"] and mmm_nnn[-1]>-min(mmm_nnn[:-1])*ddd["AB"])\
                   and float(ddd["symbols"][a]["balances"])*float(ttt[-1][4])>20:
                    lock.acquire()
                    ddd["symbols"][a]["kline_result"]=-1  #卖出
                    lock.release()
        else:
            print(f"{a}: 2不正常====")

    except Exception as e:
        print(a)
        print(e)
        pass


def assett():  #获取账户各币种余额
    global ddd, USDT, balances_id
    html=htmll(exch_bb())
    lock.acquire()
    try:
        tt=json.loads(html)
        for t in tt["balances"]:
            if float(t["free"])>0 and t["asset"] in ddd["symbols"].keys():
                ddd["symbols"][t["asset"]]["balances"]=t["free"]
            elif float(t["free"])>0 and t["asset"]=="USDT":
                USDT=float(t["free"])
                print(USDT)
        balances_id=time.time()
    except Exception as e:
        print(e)
        pass
    finally:
        lock.release()


def orderr(symbol,side,type,q_type,quantity):  #下单
    global ddd, USDT
    kk=exch_cc(symbol+"USDT",side,type,q_type,quantity)
    print(kk)
    html=htmll(kk[0], kk[1])
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
    ss.append("AccessKeyId=8390417f-qz5c4v5b6n-fadbc644-8415e")
    ss.append("SignatureMethod=HmacSHA256")
    ss.append("SignatureVersion=2")
    ss.append("Timestamp="+tt)

    ss.sort()
    urll="&".join(ss)
    urll2=uu+urll
    signature = hmac.new(b"c5432677-76d1f7f8-9454db25-040bb", urll2.encode(encoding = "utf-8"), digestmod=hashlib.sha256).digest()
    cc=base64.b64encode(signature)
    cc=quote(cc)
    return uu2+urll+"&Signature="+cc

def exch_bb():     #查询账户余额
    uu="https://api.binance.com/api/v3/account"
    uu2="recvWindow=5000&timestamp="+str(int(time.time()*1000)-ab_time)
    signature = hmac.new(Secret_Key.encode(encoding = "utf-8"), uu2.encode(encoding = "utf-8"), digestmod=hashlib.sha256).hexdigest()
    return uu+"?"+uu2+"&signature="+signature

def exch_cc(symbol,side,type,q_type,quantity):     #下单
    uu="https://api.binance.com/api/v3/order"
    #uu="https://api.binance.com/api/v3/order/test"  #测试下单
    if q_type=="b":  #base如BTC的报价下单
        uu2="symbol="+symbol+"&side="+side+"&type="+type+"&quantity="+quantity+"&recvWindow=5000&newOrderRespType=ACK&timestamp="+str(int(time.time()*1000)-ab_time)
    elif q_type=="q":  #quote如USDT的报价下单
        uu2="symbol="+symbol+"&side="+side+"&type="+type+"&quoteOrderQty="+quantity+"&recvWindow=5000&newOrderRespType=ACK&timestamp="+str(int(time.time()*1000)-ab_time)
                
    signature = hmac.new(Secret_Key.encode(encoding = "utf-8"), uu2.encode(encoding = "utf-8"), digestmod=hashlib.sha256).hexdigest()
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
        if minQty=="1.0":
            return s[:s.find(".")]
        else:
            p=s.find(".")
            p+=len(minQty)-2
            return s[:p+1]

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
    while True:
        run=False
        try:
            
            #读取all_sell文件-------
            with open('all_sell.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                ttt=json.loads(f.read())
            #读取account文件=======

            
            #校对时间并确定间隔区间--------------
            t=threading.Thread(target=exch_timee)
            t.start()
            t.join(3)
            if t.is_alive():
                stop_thread(t)
                print("强制结束线程：校对时间  "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            curr_timee=time.time()-ab_time/1000
            if ttt["all_sell"]==1 or (curr_timee%bbb[ddd["interval"]]>=10\
               and curr_timee%bbb[ddd["interval"]]<120\
               and curr_timee//bbb[ddd["interval"]]>last_time//bbb[ddd["interval"]]):  #>=15是为了时间的保守，因为有些小币种K线生成太慢
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
                    t.join(4)
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
                                    symbol,"SELL","MARKET","b",fixx(
                                        ddd["symbols"][symbol]["balances"],ddd["symbols"][symbol]["minQty"])))
                            
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
                                        if t_21>5:
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
                        t.join(4)
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
                                    symbol,"BUY","MARKET","q",fixx(
                                        str(ddd["symbols"][symbol]["buy_usdt"]),"0.01")))
                            
                            ddd["symbols"][symbol]["oth"].setDaemon(True)
                            ddd["symbols"][symbol]["oth"].start()
                            ddd["symbols"][symbol]["oth"].join(4)  #串行计算
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
                        t.join(4)
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
                print(str(run_num)+"  币安000低吸高抛_3版")
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                #设定已经第一次运行过，和上次运行时间===================
                
        except Exception as e:  #防止死锁
            print(e)


        #print(str(run_num)+"  币安后台自动交易")
        #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        time.sleep(2)
