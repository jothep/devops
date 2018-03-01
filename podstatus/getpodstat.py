#!/bin/python2.7
# -*-coding:utf-8 -*-
import os
import sys
import re
import json,urllib2

#transfer pods_string to list
def strtolist(list,str):
    list.append(str)
    print list
    return list

#write podlist to alarmfile
def listtofile(list,file):
    fo = open(file,"w")
    for i in list:
        ns = i.split('/')[0]
        pod = i.split('/')[1]
        lp = len(pod)
        if lp>17:
            podname = pod[:-17]
        else:
            podname = pod
        full =str(ns+' '+podname+'\n')
        fo.write(full)
    fo.close()

#delete duplicates row from tempfile
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

#determine whether podname belong deploy,put it to tempfile
def str_count(s):
    line = s.strip('\n')
    ns = line.split('/')[0]
    pod = line.split('/')[1]
    lp = len(pod)
    if  lp > 17:
        podname = pod[:-17]
        print podname
    else:
        podname = pod
        print podname
    full = 'echo '+ns+' '+podname+' >>/opt/podstlist'
    os.popen(full)
    
#get pod status from k8s cluster, sent status message to dingding.
 
cmd = 'kubectl get pods -a --all-namespaces -o json  | jq -r \'.items[] | select(.status.phase != "Running" or ([ .status.conditions[] | select(.type == "Ready" and .status == "False") ] | length ) == 1 ) | .metadata.namespace + "/" + .metadata.name\''
ret = str(os.popen(cmd).read())
file1 = '/opt/podstlist'
deldup(file1)
if ret:
    output = "以下pod存在状态异常:\n" + ret
    re.split('\/n',output)
    list1 = ret.split('\n')[:-1]
    listtofile(list1,file1)
#    str_count(ret)
else:
    output = ""
print output
data = {"msgtype": "text", 
   "text": {
        "content": output
     }
  }

#url = 'https://oapi.dingtalk.com/robot/send?access_token=8ac944235f58cd2ee41e89372411c1b20567e6e91a3e47a9962a41b224c22501'
url = 'https://oapi.dingtalk.com/robot/send?access_token=51b7b854096bb4b8773245f963ebba6893d38ce3f4f163b3033d864f468d98cd'

header = {
    "Content-Type": "application/json",
    "charset": "utf-8"
    }
if output:
    print "存在问题"
    sendData = json.dumps(data)
    request = urllib2.Request(url,data = sendData,headers = header)
    urlopen = urllib2.urlopen(request)
    print urlopen.read()
else:
    print "不存在pod异常。"
