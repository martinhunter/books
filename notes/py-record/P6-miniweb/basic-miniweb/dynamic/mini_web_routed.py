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
def index():
    return openfile("index.html")

@route("/login.py")
def login():
    return openfile("login.html")
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    file_name = environ['PATH_INFO']
    try:
        return decodic[file_name]()
    except Exception as ret:
        return "error occured:%s" % str(ret)
