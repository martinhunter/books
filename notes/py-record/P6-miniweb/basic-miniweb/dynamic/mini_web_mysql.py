import mysql
import re

def openfile(openf):
    with open("./templete/" + openf) as f:
        content = f.read()
    return content

# create a decorator
'''
each file_name matches a function,{'file_name':function}.
use dict to save the info
'''
decodic = {}
def route(filepath):
    def deco1(func):
        decodic[filepath] = func
        def deco2(*args, **kwargs):
            return func(*args, **kwargs)
        return deco2
    return deco1

@route("/index.py")
def index(ret):
    return openfile("index.html")

@route("/login.py")
def login(ret):
    return openfile("login.html")

# route: alldata = route(r"/add/\d+\.html")() = deoc1(alldata) = deco2
# and decodic[r"/add/\d+\.html"] = alldata
@route(r"/add/\d+\.html")
def alldata(ret):
    name = ret.group(1)
    con = mysql.connect(host='localhost', port=3306, user='root', password='mysss', database='stock_db',charset='utf8')
    cs = con.cursor()
    cs.execute("select i.code,i.short from info as i inner join focus as f\
on i.id=f.info_id;")
    stock_infos = cs.fetchall()
    cs.close()
    con.close()
    return "add (%s) ok" %name

@route(r"/del/(\d+)\.html")
def del_info(ret):
    stock_code = ret.group(1)
    con = mysql.connect(host='localhost', port=3306, user='root', password='mysss', database='stock_db',charset='utf8')
    cs = con.cursor()
    sql = """select * from info where code=%s;"""
    cs.execute(sql, (stock_code,))
    if not cs.fetchone():        
        cs.close()
        con.close()
        return “wrong info”
    
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    file_name = environ['PATH_INFO']
    try:
        for nf, cont in dicodic.items():
            ret = re.match(nf, file_name)
            if ret:
                return cont(ret)
    except Exception as ret:
        return "error occured:%s" % str(ret)
