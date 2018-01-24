#!/bin/python2.7
# -*-coding:utf-8 -*-
import os
import json
import urllib2

#common options
url1 = 'https://oapi.dingtalk.com/robot/send?access_token=51b7b854096bb4b8773245f963ebba6893d38ce3f4f163b3033d864f468d98cd'
header1 = {
    "Content-Type": "application/json",
    "charset": "utf-8"
    }
file1 = '/opt/podstlist'

#delete duplicate rows from temp file.
def deldup(file):
    rFile = open(file, 'r')
    allLine = rFile.readlines()
    rFile.close()
    wFile = open(file, 'w')
    h = {}
    for i in allLine:
        if not (h.has_key(i)) and (i != '\n') and (i != '\r\n'):
            h[i]=1
            wFile.write(i)
    wFile.close()

#delete line after pod status is Running
def delline(ns,pod,file):
    full = "sed -i -e '/"+ns+' '+pod+"/d' "+file
    ret = str(os.popen(full).read())
    #print("del %s/%s" %(ns,pod))

#Now check pods status from cluster,delete ok/none status pod from tempfile 
def checknow(file):
    rFile = open(file, 'r')
    allLine = rFile.readlines()
    rFile.close()
    list_ok = []
    list_gone = []
    for i in allLine:
        ns = i.split(' ')[0]
        pod = i.split(' ')[1][:-1]
        nspod = ns+'/'+pod+'\n'
        #print nspod
        full = 'kubectl get po --no-headers=true -n '+ns+' -l app='+pod
        ret = os.popen(full).read() 
        if ret == '':
            list_gone.append(nspod)
            delline(ns,pod,file)
        if ret != '':
            sta = filter(None, ret.split(' '))[2]
            if sta == 'Running':
                list_ok.append(nspod)
                delline(ns,pod,file)
    return list_ok,list_gone

#get err pod after checknow()
def after(file):
    rFile = open(file, 'r')
    allLine = rFile.readlines()
    rFile.close()
    list_af = []
    for i in allLine:
        nspod = i.replace(' ','/')
        list_af.append(nspod)
    return list_af

#make output json to dingding
def makejson(file):
    list_ok = []
    list_gone = []
    list_af = []
    list_ok, list_gone = checknow(file)
    list_af = after(file)
    output = ''
    if (list_ok != []):
        ok = "".join(list(list_ok))
        output += "以下pod已恢复:\n"+ok
    if (list_gone != []):
        gone = "".join(list(list_gone))
        output += "以下pod已不存在:\n"+gone
    if  (list_af != []):
        af = "".join(list(list_af))
        output += "以下pod仍未恢复:\n"+af
    return output

#sent alart message to dingding
def alart(url,header,output):
    data = {"msgtype": "text",
        "text": {
            "content": output
        }
    }
    sendData = json.dumps(data)
    request = urllib2.Request(url,data = sendData,headers = header)
    urlopen = urllib2.urlopen(request)
    print urlopen.read()

#monit pod status,do something need to do.
def recalarm(file,url,header):
    deldup(file)
    output = makejson(file)
    if output != '':
        alart(url,header,output)
    else:
        print "keep monit."
    
if __name__ == '__main__':
    recalarm(file1,url1,header1)

