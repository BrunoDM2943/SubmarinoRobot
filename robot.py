import urllib.request
import re
import time
import datetime
import socket
import sys
import threading
from flask import Flask
app = Flask(__name__)


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
                time.sleep(5)
            except:
                pass

Robot().start()
@app.route("/")
def index():
    str = ''
    for item in prices:
        str += item
        str += '<br>'
    return str

if __name__ == "__main__":
    app.run()
