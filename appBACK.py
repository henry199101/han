#!/usr/bin/env python

#encoding=utf-8



from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import logging

from QADS import QADS

import json



class S(BaseHTTPRequestHandler):



    def __init__(self):

        self.qads = QADS()



    def do_HEAD(self):

        self.send_response(200)

        self.send_header('Content-type', 'text/html')

        self.end_headers()



    def do_GET(self):

        print self.path

        paths = {

            '/foo': {'status': 200},

            '/bar': {'status': 302},

            '/baz': {'status': 404},

            '/qux': {'status': 500}

        }



        if self.path in paths:

            self.respond(paths[self.path])

        else:

            self.respond({'status': 500})

        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))



    def do_POST(self):

        print 'post',self.path

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data

        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        print post_data

        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",

                str(self.path), str(self.headers), post_data.decode('utf-8'))



        params = dict([ p.split('=')for p in post_data.decode('utf-8').split('&')])

        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        response = self.post_handler(params)

        #logging.info("post requeset result: {}".format(response))

        self.wfile.write(response)





    def post_handler(self, params):

        rst = qads.predict(params["query"])

        rstr = json.dump(rst)

        return rstr



    def respond(self, opts):

        response = self.handle_http(opts['status'], self.path)

        self.wfile.write(response)



    def handle_http(self, status_code, path):

        self.send_response(status_code)

        self.send_header('Content-type', 'text/html')

        self.end_headers()

        content = "are you ok"

        return content



def run(server_class=HTTPServer, handler_class=S, port=8080):

    logging.basicConfig(level=logging.INFO)

    server_address = ('', port)

    httpd = server_class(server_address, handler_class)

    logging.info('Starting http server...\n')

    try:

        httpd.serve_forever()

    except KeyboardInterrupt:

        pass

    httpd.server_close()

    logging.info('Stopping http server...\n')



if __name__ == '__main__':

    from sys import argv



    if len(argv) == 2:

        run(port=int(argv[1]))

    else:

        run()

