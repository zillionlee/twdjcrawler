#coding=utf-8
from django.db import models
from django.contrib import admin
# Create your models here.

class Task(models.Model):
    url = models.CharField('url',max_length=100)
    cre = models.CharField('crawler_re',max_length=300)
    status = models.SmallIntegerField('status',default=0) #0未抓取，1为已抓取

class Proxy(models.Model):
    ip = models.CharField('ip',max_length=15)
    status = models.SmallIntegerField('status',default=0) #0未校验，1为可用，2不可以
    port =  models.CharField('port',max_length=10)
    area = models.CharField('area',max_length=30)
    speed = models.FloatField('speed',null=True)

class Tclient(models.Model):
    name = models.CharField('name',max_length=20)
    add_time = models.DateTimeField('add_time',auto_now=True)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('url','status','cre')
class ProxyAdmin(admin.ModelAdmin):
    list_display = ('ip','status','port','area','speed')
class TclientAdmin(admin.ModelAdmin):
    list_display = ('name','add_time')




admin.site.register(Task,TaskAdmin)
admin.site.register(Proxy,ProxyAdmin)
admin.site.register(Tclient,TclientAdmin)