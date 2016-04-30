import urllib.request
import re
import time
import datetime
import socket
import sys
import threading


__author__ = 'Bruno'

prices = []
url = 'http://www.submarino.com.br/produto/124765021/'
regexPrice = '<span itemprop="price/salesPrice" .*>(.+?)</span>'
regexName = '<span itemprop="name">(.+?)</span>'
request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})


class Robot(threading.Thread):

    def __init__(self):
        ''' Constructor. '''
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                with urllib.request.urlopen(request) as response:
                    html_view = response.read()
                str_html = html_view.decode('UTF-8')
                price = re.findall(regexPrice, str_html)[0]
                name = re.findall(regexName, str_html)[2]
                values = 'Date={}, Name={}, Price={}'.format(datetime.datetime.now(),name, price);
                print(values)
                prices.append(values)
                time.sleep(1800)
            except:
                pass

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 80 # Arbitrary non-privileged port
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serverSocket.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

serverSocket.listen(5)
print('Open')
t = Robot()
t.daemon = True
t.start()
while True:
    print('waiting')
    c, (client_host, client_port) = serverSocket.accept()
    print('Got connection from', client_host, client_port)
    c.recv(1000)
    c.send(b'HTTP/1.0 200 OK\n')
    c.send(b'Content-Type: text/html\n')
    c.send(b'\n') # header and body should be separated by additional newline
    html_response = "<html><body><h1>Precos do Submarino</h1><br>"

    for item in prices:
        html_response += item
        html_response += '<br>'
    html_response += '</body></html>'
    c.send(str.encode(html_response))
    c.close()
serverSocket.close()

