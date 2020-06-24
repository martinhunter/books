from flask import Flask, current_app, redirect, url_for,request
from werkzeug.routing import BaseConverter

# current_app is alias of app

app = Flask(__name__,
            static_url_path="/static-url-prefix",
            static_folder="static_folder_name",
            template_folder="templates",)

'''
3 ways to config

1.
app.config.from_pyfile("config.cfg")

in config.cfg
`DEBUG = True`

2.
class Conf(object):
    DEBUG=True

app.config.from_object(Conf)

3.
app.config["DEBUG"] = True

config is actually a dictionary
'''
@app.route("/index",methods=["GET","POST"])
def index():
    '''view func'''
    name = request.form.get("name")
    age = request.form.get("age")
    form_li = request.form.get_list()
    print(request.data)  # if datatype is not form but like a json datatype
    city = request.args.get("city") # get value by key from url
    response_info = 1
    if response_info:
        return ("index page", # response body
                400, # status_code
                [("key1","value1"),("key2","value2")]) # response header. dict works as well
    else:
        resp = make_response("response body")
        resp.status = "400"
        resp.headers["key1"] = "value1"
        resp.headers["key2"] = "value2"
        return resp



def register():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    else:
        return "method can't be parsed"

@app.route("/upload")
def upload():
    file_obj = request.files.get("key_name")
    if not file_obj: return "error,upload failed"
    with open("./demo.jpg","wb") as f:
        data = file_obj.read()
        f.write(data)
        return "upload successed"
    

@app.route("/home")
def homepage():
    # redirect to indexpage
    url = url_for("index")
    
    return redirect(url)
    
# start-converter

class Reg(BaseConverter):
    def __init__(self,url_map,regex_w):
        super(Reg,self).__init__(url_map)
        # set regex rule
        self.regex = regex_w
        # converter will automatically test if real-input matches self.regex
    def to_python(self,original):
        # the return value is regexedpar and can be modified here first
        return original
    def to_url(self,original):
        # url = url_for("reg",page=234,regexedpar="regexOriginal")
        # param of url_for is original and can be modified here
        #if modified,url == modified value
        return original
        
# there might be errorhandler-dict and default-errorhandler-dict
# if defined in eh-dict,it has higher priority than d-er-dict

# abort(404) now returns handle_404 info
@app.errorhandler(404)
def handle_404(err):
    return "404 not found : %s" % err

app.url_map.converters["newconverter"] = Reg

# /index/r"regex\w*" sites will be parsed
@app.route("/index/<int:page>/<newconverter(r'regex\w*'):regexedpar>")
# @app.route("/index/<newconverter(r'regex\w*'):regexedpar>")
def reg(page,regexedpar):
    return "the page is %s.the input url is %s." % (page,regexedpar)

# end-converter

if __name__ == "__main__":
    host = "192.168.1.25"
    host2 = "0.0.0.0"
    port = 5000
    print(app.url_map)
    app.run(host2,port)
