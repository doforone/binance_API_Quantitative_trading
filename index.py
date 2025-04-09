from flask import Flask,flash,render_template,request,redirect,session,url_for,abort,Response,make_response,g
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import os

import time
import sys
import json
from datetime import timedelta
import random

from urllib import request as requestt, parse
from urllib.parse import quote

import hashlib
import hmac
import base64

from inc import fun
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

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'jpe', 'gif'])

def allowed_file(filename):
   return filename[filename.rfind('.')+1:].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*2  # 2M
#app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = "dkfsjflowemvssss"
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


@app.errorhandler(413)
def max_files(e):
    return "文件太大"

@app.errorhandler(404)
def not_found_error(error):
    return "404", 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

#-------------------------
ab_time=900  #与交易所校对时间的误差，毫秒
api_a="https://"
api_b="api-aws.huobi.pro"
Access_Key="6281fc81-309e059d-f3fe7782-d7gh5g7yng"
Secret_Key="84e90d42-706f3b5e-ed0ec417-2c91c"


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
            req = requestt.Request(url=url, data=postdata, headers=headers,
                                  origin_req_host=None, unverifiable=False,
                                  method="POST")
        else:
            req = requestt.Request(url=url, headers=headers,
                                  origin_req_host=None, unverifiable=False,
                                  method="GET")
            
        with requestt.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(e)
        return ""


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
    #ss.append("valuationCurrency=CNY")
    ss.append("valuationCurrency=USD")
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


def huobi_bb3():  #获取账户资产估值
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
    #ss.append("valuationCurrency=CNY")
    ss.append("valuationCurrency=BTC")
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


def huobi_history():  #获取账户资产估值
    uu="GET\n"+api_b+"\n/v1/order/history\n"
    uu2=api_a+api_b+"/v1/order/history?"

    #时间格式：2017-05-11T16:22:06
    tt=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(timee_ab()-28800))
    tt=quote(tt.encode("utf-8"))
    
    ss=[]
    ss.append("AccessKeyId="+Access_Key)
    ss.append("SignatureMethod=HmacSHA256")
    ss.append("SignatureVersion=2")
    ss.append("Timestamp="+tt)

    ss.append("size=100")
    ss.sort()
    
    urll="&".join(ss)
    urll2=uu+urll
    signature = hmac.new(
        Secret_Key.encode("utf-8"), urll2.encode("utf-8"),
        digestmod=hashlib.sha256).digest()
    cc=base64.b64encode(signature)
    cc=quote(cc)
    
    return uu2+urll+"&Signature="+cc
#==========================


@app.route("/set_config/", methods = ['POST'])
def set_config():
    if request.method == 'POST':
        if "pw0" in request.form.keys():
            pw=request.form["pw0"][:20]
            if pw=="set00*999":
                MN=request.form["MN"][:4]
                MN=MN.strip()
                if MN=="":
                    #MN=97
                    MN=47
                else:
                    MN=int(float(MN))

                AB=request.form["AB"][:4]
                AB=AB.strip()
                if AB=="":
                    AB=1
                else:
                    AB=float(AB)

                VV=request.form["VV"][:4]
                VV=VV.strip()
                if VV=="":
                    VV=3
                else:
                    VV=float(VV)

                AA=request.form["AA"][:4]
                AA=AA.strip()
                if AA=="":
                    AA=3
                else:
                    AA=float(AA)

                #-------------------
                with open('000火币低吸高抛/config.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    ddd=json.loads(f.read())

                ddd["MN"]=MN
                ddd["AB"]=AB
                ddd["VV"]=VV
                ddd["AA"]=AA
                
                with open('000火币低吸高抛/config.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ddd, indent=4)+"\r\n")                
                #===================

                #---------------
                with open('000币安低吸高抛/config.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    ddd=json.loads(f.read())

                ddd["MN"]=MN
                ddd["AB"]=AB
                ddd["VV"]=VV
                ddd["AA"]=AA

                with open('000币安低吸高抛/config.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ddd, indent=4)+"\r\n")
                #==================

                return "ok"
            else:
                return "pw err"
        else:
            return "pw not"
    else:
        return "method err"
    

@app.route("/huobi/", methods = ['POST'])
def huobi():
    time.sleep(0.1)
    if request.method == 'POST':
        if "pw2" in request.form.keys():
            pw=request.form["pw2"][:20]
            if pw=="huobi000*999":
                rrr={}
                rrr2=[]
                exch_timee()
                bb=huobi_bb()
                html=htmll(bb)
                ttt=json.loads(html)
                for tt in ttt["data"]["list"]:
                    if tt["currency"]=="usdt" and tt["type"]=="trade":
                        rrr["usdt"]=tt["balance"]
                        break

                bb=huobi_bb2()
                html=htmll(bb)
                ttt=json.loads(html)
                rrr["total_CNY"]=ttt["data"]["balance"]

                bb=huobi_bb3()
                html=htmll(bb)
                ttt=json.loads(html)
                rrr["total_BTC"]=ttt["data"]["balance"]
                
                cc=huobi_history()
                html=htmll(cc)
                ttt=json.loads(html)
                if ttt["status"]=="ok":
                    for tt in ttt["data"]:
                        #print(tt)
                        if tt["type"]=="buy-market":
                            rrr2.append(
                                "●"+time.strftime(
                                    "%Y-%m-%d %H:%M:%S", time.localtime(
                                        tt["finished-at"]/1000))+" "+tt["type"]+" "+tt["symbol"]+" "+tt["amount"])
                        else:
                            rrr2.append(
                                time.strftime(
                                    "%Y-%m-%d %H:%M:%S", time.localtime(
                                        tt["finished-at"]/1000))+" "+tt["type"]+" "+tt["symbol"]+" "+tt["amount"])

                ddd3=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                return render_template("huobi.html", ddd=rrr, ddd2=rrr2, ddd3=ddd3)
            else:
                return "pw err"
        else:
            return "pw not"
    else:
        return "method err"


@app.route("/huobi_all_set/", methods = ['POST'])
def huobi_all_set():
    if request.method == 'POST':
        if "pw3" in request.form.keys() and "ttt" in request.form.keys():
            pw=request.form["pw3"][:20]
            if pw=="sell000*999":
                ttt=request.form["ttt"][:10]
                ttt=ttt.strip()
                ttt=ttt.lower()
                #---------------
                with open('000火币低吸高抛/config.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    ddd=json.loads(f.read())

                if ttt=="":
                    for symbol in ddd["symbols"].keys():
                        ddd["symbols"][symbol]["kline_id"]=0
                        ddd["symbols"][symbol]["buy_price"]=0
                        ddd["symbols"][symbol]["sub_price"]=0
                else:
                    ddd["symbols"][ttt]["kline_id"]=0
                    ddd["symbols"][ttt]["buy_price"]=0
                    ddd["symbols"][ttt]["sub_price"]=0
                    
                with open('000火币低吸高抛/config.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ddd, indent=4)+"\r\n")
                #==================
                
                ttt={"all_set":1}
                with open('000火币低吸高抛/all_set.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ttt, indent=4)+"\r\n")
                #==================
                    
                return "sell:ok"
            
            elif pw=="buy000*999":
                ttt=request.form["ttt"][:10]
                ttt=ttt.strip()
                ttt=ttt.lower()
                #---------------
                with open('000火币低吸高抛/config.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    ddd=json.loads(f.read())

                if ttt=="":
                    for symbol in ddd["symbols"].keys():
                        if ddd["symbols"][symbol]["buy_price"]==0:
                            ddd["symbols"][symbol]["kline_id"]=0
                            ddd["symbols"][symbol]["buy_price"]=-1
                            ddd["symbols"][symbol]["sub_price"]=0
                else:
                    if ddd["symbols"][ttt]["buy_price"]==0:
                        ddd["symbols"][ttt]["kline_id"]=0
                        ddd["symbols"][ttt]["buy_price"]=-1
                        ddd["symbols"][ttt]["sub_price"]=0
                    
                with open('000火币低吸高抛/config.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ddd, indent=4)+"\r\n")
                #==================
                
                ttt={"all_set":1}
                with open('000火币低吸高抛/all_set.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ttt, indent=4)+"\r\n")
                #==================
                    
                return "buy:ok"
            else:
                return "pw err"
        else:
            return "pw not"
    else:
        return "method err"


@app.route("/huobi_all_set_close/", methods = ['POST'])
def huobi_all_set_close():
    if request.method == 'POST':
        if "pw2_01" in request.form.keys():
            pw2_01=request.form["pw2_01"][:20]
            if pw2_01=="set000*999":
                ttt={"all_set":-1}
                with open('000火币低吸高抛/all_set.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ttt, indent=4)+"\r\n")
                return "set: close"
            else:
                return "pw err"
        else:
            return "pw not"
    else:
        return "method err"


@app.route("/huobi_all_set_open/", methods = ['POST'])
def huobi_all_set_open():
    if request.method == 'POST':
        if "pw2_01" in request.form.keys():
            pw2_01=request.form["pw2_01"][:20]
            if pw2_01=="set000*999":
                ttt={"all_set":0}
                with open('000火币低吸高抛/all_set.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ttt, indent=4)+"\r\n")
                return "set: open"
            else:
                return "pw err"
        else:
            return "pw not"
    else:
        return "method err"


@app.route("/huobi_all_set_look/")
def huobi_all_set_look():
    with open('000火币低吸高抛/all_set.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ddd=json.loads(f.read())
    if (d:=ddd["all_set"])==0:
        r="正常状态"
    elif d==1:
        r="立即执行"
    elif d==-1:
        r="暂停"
        
    return r
    

@app.route("/bian_all_set/", methods = ['POST'])
def bian_all_set():
    if request.method == 'POST':
        if "pw" in request.form.keys() and "ttt" in request.form.keys():
            pw=request.form["pw"][:20]
            if pw=="sell00*999":
                ttt=request.form["ttt"][:10]
                ttt=ttt.strip()
                ttt=ttt.upper()
                #---------------
                with open('000币安低吸高抛/config.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    ddd=json.loads(f.read())
                    
                if ttt=="":
                    for symbol in ddd["symbols"].keys():
                        ddd["symbols"][symbol]["kline_id"]=0
                        ddd["symbols"][symbol]["buy_price"]=0
                        ddd["symbols"][symbol]["sub_price"]=0
                else:
                    ddd["symbols"][ttt]["kline_id"]=0
                    ddd["symbols"][ttt]["buy_price"]=0
                    ddd["symbols"][ttt]["sub_price"]=0
                    
                with open('000币安低吸高抛/config.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ddd, indent=4)+"\r\n")
                #==================
                
                ttt={"all_set":1}
                with open('000币安低吸高抛/all_set.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ttt, indent=4)+"\r\n")
                #==================
                    
                return "sell:ok"
            
            elif pw=="buy00*999":
                ttt=request.form["ttt"][:10]
                ttt=ttt.strip()
                ttt=ttt.upper()
                #---------------
                with open('000币安低吸高抛/config.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                    ddd=json.loads(f.read())
                    
                if ttt=="":
                    for symbol in ddd["symbols"].keys():
                        if ddd["symbols"][symbol]["buy_price"]==0:
                            ddd["symbols"][symbol]["kline_id"]=0
                            ddd["symbols"][symbol]["buy_price"]=-1
                            ddd["symbols"][symbol]["sub_price"]=0
                else:
                    if ddd["symbols"][ttt]["buy_price"]==0:
                        ddd["symbols"][ttt]["kline_id"]=0
                        ddd["symbols"][ttt]["buy_price"]=-1
                        ddd["symbols"][ttt]["sub_price"]=0
                    
                with open('000币安低吸高抛/config.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ddd, indent=4)+"\r\n")
                #==================
                
                ttt={"all_set":1}
                with open('000币安低吸高抛/all_set.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ttt, indent=4)+"\r\n")
                #==================
                    
                return "buy:ok"
            else:
                return "pw err"
        else:
            return "pw not"
    else:
        return "method err"


@app.route("/bian_all_set_close/", methods = ['POST'])
def bian_all_set_close():
    if request.method == 'POST':
        if "pw_01" in request.form.keys():
            pw_01=request.form["pw_01"][:20]
            if pw_01=="set00*999":
                ttt={"all_set":-1}
                with open('000币安低吸高抛/all_set.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ttt, indent=4)+"\r\n")
                return "set: close"
            else:
                return "pw err"
        else:
            return "pw not"
    else:
        return "method err"


@app.route("/bian_all_set_open/", methods = ['POST'])
def bian_all_set_open():
    if request.method == 'POST':
        if "pw_01" in request.form.keys():
            pw_01=request.form["pw_01"][:20]
            if pw_01=="set00*999":
                ttt={"all_set":0}
                with open('000币安低吸高抛/all_set.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                    f.write(json.dumps(ttt, indent=4)+"\r\n")
                return "set: open"
            else:
                return "pw err"
        else:
            return "pw not"
    else:
        return "method err"


@app.route("/bian_all_set_look/")
def bian_all_set_look():
    with open('000币安低吸高抛/all_set.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ddd=json.loads(f.read())
    if (d:=ddd["all_set"])==0:
        r="正常状态"
    elif d==1:
        r="立即执行"
    elif d==-1:
        r="暂停"
        
    return r


@app.route("/")
def index():
    print("bi.kefabu.com 币安量化交易")
    return render_template("login.html")


@app.route("/login_prg/", methods = ['POST', 'GET'])
def login_prg():
    time.sleep(0.1)
    if request.method == 'POST':
        if "account" in request.form.keys() and "pw" in request.form.keys():
            account=request.form["account"][:20]
            pw=request.form["pw"][:20]
            pw=hashlib.md5(pw.encode(encoding='UTF-8')).hexdigest()
            with open('account.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                accounts=json.loads(f.read())
            if account in accounts.keys():
                if accounts[account]["pw"]==pw:
                    session["account"] = account
                    session["on"]=accounts[account]["on"]
                    session["API_Key"]=accounts[account]["API_Key"]
                    session["Secret_Key"]=accounts[account]["Secret_Key"]
                    session.permanent = True
                    app.permanent_session_lifetime = timedelta(minutes=20)

                    return redirect(url_for('face'))
                else:
                    return render_template("login.html", title="错误的用户名或密码，请重新登录（注意区分大小写）。")
            else:
                return render_template("login.html", title="错误的用户名或密码，请重新登录（注意区分大小写）。")
        else:
            return render_template("login.html", title="错误的用户名或密码，请重新登录（注意区分大小写）。")
    else:
        return render_template("login.html", title="错误的登录方式，请重新登录（注意区分大小写）。")

@app.route("/face/")
def face():
    if "account" in session:
        with open('config\\'+session["account"]+'_a.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
            symbols1=json.loads(f.read())
        return render_template("face.html", symbols0=fun.aa.keys(), symbols1=symbols1)
    else:
        return render_template("login.html", title="登录超时，请重新登录（注意区分大小写）。")

@app.route("/pw/")
def pw():
    if "account" in session:
        return render_template("pw.html")
    else:
        return render_template("login.html", title="登录超时，请重新登录。")

@app.route("/pw_prg/", methods = ['POST'])
def pw_prg():
    if request.method == 'POST':
        if "account" in session and "on" in session:
            on=request.form["R1"]
            pw=request.form["pw"][:20]
            pw2=request.form["pw2"][:20]
            API_Key=request.form["API_Key"][:80]
            Secret_Key=request.form["Secret_Key"][:80]
            if pw!=pw2:
                return render_template("pw.html",title="校验密码与新密码不一致，请重新输入。")
            else:
                try:
                    #判断lock是否加锁，加锁==1时，证明别的程序正在写入，等待直至0------------
                    while True:
                        with open('lock.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                            lock_txt=json.loads(f.read())
                            if lock_txt["lock"]==1:
                                time.sleep(0.01)
                            else:
                                lock_txt["lock"]=1
                                with open('lock.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                                    f.write(json.dumps(lock_txt, indent=4)+"\r\n")
                                break
                    #判断lock是否加锁，加锁==1时，证明别的程序正在写入，等待直至0=============

                    #读取，修改，并写入account文件-------
                    with open('account.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                        accounts=json.loads(f.read())

                    if on=="1":
                        accounts[session["account"]]["on"]=1
                    else:
                        accounts[session["account"]]["on"]=0

                    if pw!="":
                        accounts[session["account"]]["pw"]=hashlib.md5(pw.encode(encoding='UTF-8')).hexdigest()

                    accounts[session["account"]]["API_Key"]=API_Key
                    accounts[session["account"]]["Secret_Key"]=Secret_Key

                    with open('account.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                        f.write(json.dumps(accounts, indent=4)+"\r\n")
                    #读取，修改，并写入account文件=======

                    title="修改成功，请重新登录。"
                except Exception as e:
                    #print(e)
                    title="发生错误，请重新登录。"
                finally:
                    #解锁-------------------
                    lock_txt={}
                    lock_txt["lock"]=0
                    with open('lock.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                        f.write(json.dumps(lock_txt, indent=4)+"\r\n")
                    #解锁===================
                    session.pop('account', None)
                    session.pop('on', None)
                    session.pop('API_Key', None)
                    session.pop("Secret_Key", None)
                    return render_template("login.html", title=title)

@app.route("/set111/", methods = ['GET'])
def set111():
    if "account" in session:
        if request.method == 'GET':
            symbol=request.args["symbol"]
            on=request.args["on"]
            with open('config\\'+session["account"]+'_a.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                symbols=json.loads(f.read())
            if symbol in symbols.keys():
                return render_template("set111.html", symbol=symbol, symbol_config=symbols[symbol], on=on)
            else:
                return render_template("set111.html", symbol=symbol, symbol_config=fun.symbol_config, on=on)
        else:
            return render_template("login.html", title="非法操作，请重新登录。")
    else:
        return render_template("login.html", title="登录超时，请重新登录。")

@app.route("/set111_prg/", methods = ['POST'])
def set111_prg():
    if "account" in session:
        if request.method == 'POST':
            symbol=request.form["symbol"][:6]
            R1=request.form["R1"]
            p=request.form["p"]
            per=request.form["per"]
            q_type=request.form["q_type"]
            q=request.form["q"]
            again=request.form["R2"]
            if again in ["60", "300", "900", "1800", "3600"]:
                pass
            else:
                again="60"

            if symbol in fun.aa.keys():
                if fun.is_number(p) and fun.is_number(per) and fun.is_number(q):
                    p=float(p)
                    per=float(per)
                    q=float(q)
                    if p>0 and per>0 and q>0:
                        if q_type=="q" and q<10:
                            flash('下单量不能小于10USDT，请重新设定。')
                            return redirect(url_for('face'))
                        else:
                            if q_type=="b":
                                if q<float(fun.aa[symbol]["minQty"]) or q>float(fun.aa[symbol]["maxQty"]):
                                    flash('下单量范围应为：'+fun.aa[symbol]["minQty"]+' -- '+fun.aa[symbol]["maxQty"]+'，请重新设定。')
                                    return redirect(url_for('face'))
                                else:
                                    q=fun.fixx(str(q),fun.aa[symbol]["minQty"])
                                    q=float(q)
                            #----------------------
                            try:
                                #判断lock是否加锁，加锁==1时，证明别的程序正在写入，等待直至0------------
                                while True:
                                    with open('lock.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                                        lock_txt=json.loads(f.read())
                                        if lock_txt["lock"]==1:
                                            time.sleep(0.01)
                                        else:
                                            lock_txt["lock"]=1
                                            with open('lock.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                                                f.write(json.dumps(lock_txt, indent=4)+"\r\n")
                                            break
                                #判断lock是否加锁，加锁==1时，证明别的程序正在写入，等待直至0=============

                                #读取，修改，并写入account，config文件-------
                                with open('config\\'+session["account"]+'_a.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                                    symbols=json.loads(f.read())

                                if R1=="1":
                                    if symbol not in symbols.keys():
                                        symbols[symbol]={}
                                    symbols[symbol]["p"]=p
                                    symbols[symbol]["per"]=per
                                    symbols[symbol]["q_type"]=q_type
                                    symbols[symbol]["q"]=q
                                    symbols[symbol]["time"]=int(time.time())
                                    symbols[symbol]["oth"]=0
                                    symbols[symbol]["again"]=int(again)
                                else:
                                    if symbol in symbols.keys():
                                        symbols.pop(symbol)

                                with open('config\\'+session["account"]+'_a.txt', 'w', encoding='utf-8-sig', newline='\r\n') as f:
                                    f.write(json.dumps(symbols, indent=4)+"\r\n")
                                #***************************
                                with open('account.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
                                    accounts=json.loads(f.read())

                                accounts[session["account"]]["re_config"]=1

                                with open('account.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                                    f.write(json.dumps(accounts, indent=4)+"\r\n")
                                #读取，修改，并写入account，config文件=======

                                flash('设置成功。')
                            except Exception as e:
                                print(e)
                                flash('发生错误，请重新设定。')
                                flash(e)
                            finally:
                                #解锁-------------------
                                lock_txt={}
                                lock_txt["lock"]=0
                                with open('lock.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                                    f.write(json.dumps(lock_txt, indent=4)+"\r\n")
                                #解锁===================
                                return redirect(url_for('face'))
                            #====================================
                    else:
                        flash('输入的数字要大于0，请重新设定。')
                        return redirect(url_for('face'))
                else:
                    flash('输入的并非完全小写数字，请重新设定。')
                    return redirect(url_for('face'))
            else:
                flash('输入的交易对暂时不支持，请重新设定。')
                return redirect(url_for('face'))
    else:
        return render_template("login.html", title="登录超时，请重新登录。")

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5001, debug=True, threaded=True)
   #app.run(threaded=False, processes=3)  启用三个进程，即三个CPU
   #app.run(debug=True,threaded=True)
