def openfile(openf):
    with open("./templete/" + openf) as f:
        content = f.read()
    return content
def index():
    return openfile("index.html")
def login():
    return openfile("login.html")
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    file_name = environ['PATH_INFO']
    if file_name == "/index.py":
        index()
    elif file_name == "/login.py":
        login()
    else:
        return "no match"
