import socket
import re
import multiprocessing
import sys
import ast

class WSGIServer(object):
    '''docstring basic dynamic web server'''
    def __init__(self, port, app, staticpath):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_server_socket.bind(('', port))
        self.tcp_server_socket.listen(128)
        self.application = app
        self.staticpath = staticpath

    def service_client(self, new_socket):
        '''找到所请求的目标文件所在路径'''
        request = new_socket.recv(1024).decode("utf-8")
        request_lines = request.splitlines()
        print("")
        print(">"*20)
        print(request_lines)
        

        file_name = ""
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        if ret:
            file_name = ret.group(1)
            if file_name == "/":
                file_name = "/index.html"
        # static webpage
        if not file_name.endswith(".py"):
            try:
                f = open(self.staticpath + file_name, "rb")
            except:
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "file not found"
                new_socket.send(response.encode("utf-8"))
            else:
                html_content = f.read()
                f.close()
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                new_socket.send(response.encode("utf-8"))
                new_socket.send(html_content)
        # dynamic webpage
        else:
            env = dict()
            env['PATH_INFO'] = file_name
            body = self.application(env, self.set_response_header)
            
            header = "HTTP/1.1 %s\r\n" %self.status
            for temp in self.headers:
                header += "%s:%s\r\n" %(temp[0],temp[1])
            header += "\r\n"
            response = header + body
            new_socket.send(response.encode("utf-8"))
            
        new_socket.close()

    def set_response_header(self, status, headers):
        '''函数传递给application并由框架中的application函数设置status和headers'''
        self.status = status
        self.headers = headers
        
    def main_run(self):
        while True:
            new_socket, client_addr = self.tcp_server_socket.accept()
            p = multiprocessing.process(target=self.service_client, args=(new_socket,))
            p.start()
            new_socket.close()
        self.tcp_server_socket.close()


def main():
    '''传入参数port，框架名称，框架名称下的application函数'''
    if len(sys.argv) == 3:
        try:
            port = int(sys.argv[1])
            frame_app_name = sys.argv[2]
        except Exception as ret:
            print("wrong port")
            return
    else:
        print("wrong input")
    # input python3 web-server.py 3614 mini_web:application
    ret = re.match(r"([^:]+):(.*)", frame_app_name)
    if ret:
        frame_name = ret.group(1)
        app_name = ret.group(2)
    else:
        print("wrong input")
        return
    with open("./web_server.conf") as f:
        dic_info = ast.literal_eval(f.read())
    sys.path.append(dic_info['dynamic_path'])
    frame = __import__(frame_name)
    app = getattr(frame, app_name)

    
    wsgi = WSGIServer(port, app, dic_info['static_path'])
    wsgi.main_run()


if __name__ == '__main__':
    main()
