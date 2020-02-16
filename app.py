from flask import Flask,render_template,send_file,request,url_for,session,g
from flask_bootstrap import Bootstrap
import config
from JobJudge_Pre import *
import csvFn
import random
import os
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(config)
app.secret_key='adfadfSADFA5113'
path = r'data.csv'  # 文件打开路径
def chance(list):
    slice = random.choice(list)
    return slice
def addpage(page):
    page = page+1
    return page
def reducepage(page):
    page = page-1
    return page
env = app.jinja_env
env.filters['chance'] = chance
env.filters['addpage'] = addpage
env.filters['reducepage'] = reducepage
file_dir = r'map'
file_dir_fangjia = r'fangjia'
# Info=SeniorityJudgeFn('0',Info)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        position = request.form.get('position')
        money = request.form.get('money')
        xingzhi = request.form.get('xingzhi')
        daiyu = request.form.get('daiyu')
        xueli = request.form.get('xueli')
        jingyan = request.form.get('jingyan')
        session['money'] = money
        session['position'] = position
        session['xingzhi'] = xingzhi
        session['daiyu'] = daiyu
        session['xueli'] = xueli
        session['jingyan'] = jingyan
        Info = csvFn.csvReadFn(path)  # 读取csv
        Judge = JudgeFn()  # 实例化JudgeFn 传入Info
        Info = Judge.Seniority(Info, jingyan or ' ')  # 传入进来工作经验 字符串类型的数字
        Info = Judge.Money(Info, money or ' ')  # 传入期望薪资单位为k/月 字符串类型数字
        Info = Judge.Edu(Info, xueli or ' ')  # 传入学历 下拉列表固定值
        Info = Judge.CompanyType(Info, xingzhi or ' ')  # 传入公司类型 下拉列表固定值
        #Info = Judge.CompanySize(Info, '50-150人')  # 传入公司规模 下拉列表固定值
        Info = Judge.JobWelfare(Info, daiyu or ' ')  # 传入公司福利 下拉列表固定值
        #Info = Judge.City(Info, '上海')  # 传入城市
        Info = Judge.Position(Info,position or ' ')
        Info, PageNum = DataShow(Info, 9,1)
        return render_template('index.html',info = Info.values,page=1)
    return render_template('index.html',page = 1)


@app.route('/<int:page>/')
def paging(page):
    position,money,xingzhi,daiyu,xueli,jingyan = session.get('position'),session.get('money'),session.get('xingzhi'),session.get('daiyu'),session.get('xueli'),session.get('jingyan'),
    Info = csvFn.csvReadFn(path)  # 读取csv
    Judge = JudgeFn()  # 实例化JudgeFn 传入Info
    Info = Judge.Seniority(Info, jingyan or ' ')  # 传入进来工作经验 字符串类型的数字
    Info = Judge.Money(Info, money or ' ')  # 传入期望薪资单位为k/月 字符串类型数字
    Info = Judge.Edu(Info, xueli or ' ')  # 传入学历 下拉列表固定值
    Info = Judge.CompanyType(Info, xingzhi)  # 传入公司类型 下拉列表固定值
    # Info = Judge.CompanySize(Info, '50-150人')  # 传入公司规模 下拉列表固定值
    Info = Judge.JobWelfare(Info, daiyu or ' ')  # 传入公司福利 下拉列表固定值
    # Info = Judge.City(Info, '上海')  # 传入城市
    Info = Judge.Position(Info, position)
    print(Info)
    Info, PageNum = DataShow(Info, 9, page)
    print(Info)


    return render_template('index.html',info = Info.values,page=page)
@app.route('/map/<city>')
def city_map(city):
    for root, dirs, files in os.walk(file_dir):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if name in city:
                return send_file('map/%s.html' % name)
@app.route('/fangjia/<city>')
def city_fangjia(city):
    for root, dirs, files in os.walk(file_dir):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if name in city:
                return send_file('fangjia/%s.html' % name)


@app.route('/map')
def map():
    return send_file('/untitled/map/qcwy_pre.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500


if __name__ == '__main__':
    app.run(debug=1)
