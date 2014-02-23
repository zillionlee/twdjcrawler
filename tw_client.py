#coding=utf-8
__author__ = 'zillionlee'
#User: zillionlee
#Date: 14-1-26
from twisted.internet.protocol import ClientFactory,Protocol
from twisted.internet import reactor
import sys,os
import time
project_path= os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
#print project_path
if project_path not in sys.path :
    sys.path.append(project_path)
    sys.path.append(os.path.join(project_path,'twdjcrawler').replace('\\','/'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twdjcrawler.settings")

from django.db.models import get_models
from django.core import serializers
import json
loaded_models = get_models()
def DoCrawl(data):
    import re,urllib2,time
    proxylist = []
    d = json.loads(data)
    p = re.compile(d[0]['fields']['cre'])
    req = urllib2.urlopen(d[0]['fields']['url'])
    result = req.read()
    matchs = p.findall(result)
    for row in matchs:
        try:
            ip= row[0]
            port=row[1]
            agent=row[2].decode('gb2312').encode('utf-8')
            address=row[3].decode('gb2312').encode('utf-8')
            l = [ip,port,agent,address]
            proxylist.append(l)
        except Exception,e:
            continue
    #check
    timeout = 3
    testurl = r"http://www.baidu.com/"
    test_str = '030173'
    checkedProxylist = []
    cookies = urllib2.HTTPCookieProcessor()
    for proxy in proxylist[:10]:
        proxy_handler = urllib2.ProxyHandler({"http":r'http://%s:%s' %(proxy[0],proxy[1])})
        opener = urllib2.build_opener(cookies,proxy_handler)
        urllib2.install_opener(opener)
        t1 = time.time()
        try:
            req = urllib2.urlopen(testurl,timeout=timeout)
            result = req.read()
            timeused =round(time.time() - t1,4)
            pos = result.find(test_str)
            if pos>1:
                #checkedProxylist.append([proxy[0],proxy[1],proxy[2],proxy[3],timeused])
                checkedProxylist.append({'ip':proxy[0],'port':proxy[1],'area':proxy[3],'speed':timeused})
            else:
                continue
        except:
            continue
    proxy_dic={}
    i=0
    for ck in checkedProxylist:
        proxy_dic[i]=ck
        i+=1
    return proxy_dic




class GetTask(Protocol):
    def connectionMade(self):
        pass
        #self.transport.write("hi,server")
    def dataReceived(self, data):
        print data
        crawresult = DoCrawl(data)
        if crawresult !=[]:
            self.transport.write(json.dumps(crawresult))
        else:print "no result"

class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print "connection starting..."
    def buildProtocol(self, addr):
        print addr
        return GetTask()
    def clientConnectionLost(self, connector, reason):
        print "lose reason",reason
    def clientConnectionFailed(self, connector, reason):
        print "faild reason",reason

#def fun():
#    print "call later"

#reactor.callLater(1,fun)
reactor.connectTCP('127.0.0.1',8001,EchoClientFactory())
reactor.run()
