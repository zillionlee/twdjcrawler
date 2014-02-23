#coding=utf-8
__author__ = 'zillionlee'
#User: zillionlee
#Date: 14-1-26
from twisted.internet import reactor
from twisted.internet.protocol import Factory,Protocol
import sys,os
import json
project_path= os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
#print project_path
if project_path not in sys.path :
    sys.path.append(project_path)
    sys.path.append(os.path.join(project_path,'twdjcrawler').replace('\\','/'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twdjcrawler.settings")

from django.db.models import get_models
from django.core import serializers
loaded_models = get_models()
tasks=[]
from crawler.models import Task,Proxy
def get_tasks():
        #while True:
        #time.sleep(5)
        tks = Task.objects.filter(status=0)
        tasks.extend(tks)
        print tasks
class SendTask(Protocol):
    global tasks
    def connectionMade(self):
        try:
            tobj = tasks.pop()
            if tobj is not None:
                self.transport.write(serializers.serialize("json",[tobj,]))
                tobj.status = 1
                tobj.save()
        except Exception:
            self.transport.write("no task")
        #self.transport.loseConnection()

    def dataReceived(self, data):
        d = json.loads(data)
        #print type(d)
        for key,val in d.iteritems():
            proxy = Proxy()
            proxy.ip=val['ip']
            proxy.port=val['port']
            proxy.area = val['area']
            proxy.status = 1
            proxy.speed = val['speed']
            proxy.save()
        print "received!"
        #self.transport.write("haha:"+ data)


factory = Factory()
factory.protocol = SendTask

reactor.callLater(1,get_tasks)
reactor.listenTCP(8001,factory)
reactor.run()
