from flask import Flask,flash,render_template,request,redirect,session,url_for,abort,Response,make_response,g
from werkzeug import secure_filename
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

@app.route("/")
def index():
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
    app.config['SERVER_NAME'] ='bi.shang800.com:5002'
    app.run(host="0.0.0.0", port=5002, debug=True, threaded=True, ssl_context=('path/1_bi.shang800.com_bundle.crt', 'path/2_bi.shang800.com.key'))
    #app.run(host="0.0.0.0", port=5002, debug=False, threaded=True, ssl_context=('path/1_bi.shang800.com_bundle.crt', 'path/2_bi.shang800.com.key'))
    #app.run(threaded=False, processes=3)  启用三个进程，即三个CPU
    #app.run(debug=True,threaded=True)
