__author__ = 'liujiahua'
from fcloud_api import app
from gevent.pywsgi import WSGIServer

if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=8181,debug=True)
    http_server = WSGIServer(('0.0.0.0', 8181), app)
    http_server.serve_forever()