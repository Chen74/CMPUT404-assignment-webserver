#  coding: utf-8
import mimetypes
import socketserver
import os
from datetime import date


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


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK", 'utf-8'))
        header = self.data.decode().split("\n")
        info = header[0].split()
        # print(header.split('\n'))
        file_path = './www'
        # print(file_path)
        count = 0
        if info[0].upper() == "GET":
            file_path += info[1]
            print(file_path)
            if os.path.isfile(file_path):
                mimetype = mimetypes.guess_type(file_path)
                self.successful_200(file_path, mimetype)
            else:
                if file_path.endswith("/"):
                    # if ".html" in file_path or ".css" in file_path:
                    print(file_path)
                    file_path += "index.html"
                    mimetype = mimetypes.guess_type(file_path)
                    self.successful_200(file_path, mimetype)
                else:
                    print(file_path)
                    file_path += "index.html"
                    mimetype = mimetypes.guess_type(file_path)
                    self.successful_200(file_path, mimetype)

            # path = os.path.realpath(os.getcwd() + "/www" + file_path)

            # if ".." in "./www" + file_path:
            #     count = count - 1
            #     if count < 0:
            #         self.not_found_404()

        else:
            self.not_allowed_405()

    def not_found_404(self):
        info = "HTTP/1.1 404 Not Found\r\n"
        self.request.sendall(bytearray(info, 'utf-8'))

    def not_allowed_405(self):
        info = "HTTP/1.1 405 Method Not Allowed\r\n"
        self.request.sendall(bytearray(info, 'utf-8'))

    def successful_200(self, path, ftype):
        info = "HTTP/1.1 200 OK\r\n"
        # ftype = str(self.type_check(path))
        content_type = "Content-Type: " + str(ftype) + "; charset=UTF-8\r\n"
        file = open(path, 'r')
        content = file.read()
        file.close()
        response = info + content_type + content
        self.request.sendall(bytearray(response, 'utf-8'))

    def redirect_301(self, path):
        info = '301 Moved Permanently\r\n'
        location = "Location: %s\r\n".format(path)
        ftype = str(self.type_check(path))
        content_type = "Content-Type: " + ftype + "; charset=UTF-8\r\n"
        Date = "Date: %s\r\n".format(date.today().strftime("%d/%m/%Y"))
        response = info + location + content_type + Date
        self.request.sendall(bytearray(response + open(path).read(), 'utf-8'))

    def type_check(self, path):
        if ".css" in path or ".plain" in path:
            file_type = "text/css"
            return file_type
        elif ".html" in path:
            file_type = "text/html"
            return file_type


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
# https://docs.python.org/2/library/os.path.html
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
# https://stackoverflow.com/questions/22839278/python-built-in-server-not-loading-css