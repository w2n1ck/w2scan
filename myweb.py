#!/usr/bin/env python
# coding=utf-8

from flask import Flask,render_template,request
import re
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

empty=False

app = Flask(__name__)
#连接数据库操作
#db = MySQLdb.connect("127.0.0.1","root","","123456",charset='utf8' )
#cursor = db.cursor()

@app.route('/',methods=["get","post"])
def index():
    return render_template('index.html',title="首页")

@app.route('/scanner',methods=["get","post"])
def scanner():
    if request.method == 'POST':
        args = request.form.get('args')
        #return args
        cmd = "python main.py %s" % args

        os.system("python main.py %s" % args)
        time.sleep(1000)
        report_path = '/root/bishe/source/plugins/'
        #if os.listdir(report_path):
            #return render_template('scanner_result.html',title="报告")
        #else:
        #return render_template('scanner_result.html',title="报告")
        try:
            os.system("python main.py %s" % args)
            raise Exception('scanning')
        except Exception:
            return render_template('scanner_result.html',title="报告")
        finally:
            return render_template('scanner_result.html',title="报告")
        #data =  poc_model.w2scan_main(target,plugin,level)
        #return render_template('scanner_result.html',title="报告")
        #return app.send_static_file('w2scan_poc_result.html')
    else:
        return render_template('scanner.html',title="扫描器")

if __name__ == '__main__':
    app.run(debug=True)
