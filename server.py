#  coding: utf-8
import os.path
import socketserver
from datetime import datetime

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
from datetime import date


# check if the method is "GET
def correct_method(method):
    if method.upper() == "GET":
        return True
    else:
        return False


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        headers = self.data.decode().split("\n")
        # split the herder information to get the method and the file path
        info = headers[0].split()
        method = info[0]
        if correct_method(method):
            file_path = "./www" + info[1]
            if '../' not in file_path:
                # raise 404 error if ".." in file path
                if os.path.isdir(file_path):
                    # check if the path is a directory, if it is, check if it ends with "/"
                    if file_path.endswith("/"):
                        file_path += "index.html"
                    elif not file_path.endswith('/'):
                        # redirect to proper path if the file path does not ends with "/"
                        self.redirect_301()
                        file_path += "/index.html"
                    ftype = self.type_check(file_path)
                    filename = open(file_path, "r")
                    content = filename.read()
                    filename.close()
                    self.ok_200(ftype)
                    self.request.sendall(bytearray(content, "utf-8"))

                # check if the path is a file
                elif os.path.isfile(file_path):
                    filename = open(file_path, "r")
                    content = filename.read()
                    filename.close()
                    ftype = self.type_check(file_path)
                    self.ok_200(ftype)
                    self.request.sendall(bytearray(content, "utf-8"))
                else:
                    self.not_found_404()
            else:
                self.not_found_404()
        else:
            self.not_allowed_405()

    def type_check(self, path):
        if ".css" in path:
            return "text/css"
        elif ".html" in path:
            return "text/html"

    def ok_200(self, ftype):
        info = "HTTP/1.1 200 OK\r\n"
        content_type = "Content-Type: " + ftype + "; charset=UTF-8\r\n"
        Date = f"Date: {datetime.now()}\r\n\r\n"
        response = info + content_type + Date
        self.request.sendall(bytearray(response, 'utf-8'))

    def not_allowed_405(self):
        info = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        self.request.sendall(bytearray(info, 'utf-8'))

    def not_found_404(self):
        info = "HTTP/1.1 404 Not Found\r\n\r\n"
        self.request.sendall(bytearray(info, 'utf-8'))

    def redirect_301(self):
        info = 'HTTP/1.1 301 Moved Permanently\r\n'
        Date = f"Date: {datetime.now()}\r\n\r\n"
        response = info + Date
        self.request.sendall(bytearray(response, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
