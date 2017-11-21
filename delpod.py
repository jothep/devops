
import os
import sys
#import json

#脚本在有kubectl的主机上运行
#将所有pod信息存入/tmp/abc.t
os.system("kubectl get po --all-namespaces |sed '1d;$d' |awk '{print $4,$1,$2}' > /tmp/abc.t")

#将所有检测到unknown状态的pod，通过kubectl删除
for line in open("/tmp/abc.t"):
    if line.startswith('Unknown'):
        pod = line.split()[2]
        ns = line.split()[1]
#        print('POD:' + pod + ' ' + 'NAMESPACE:'+ ns + 'DELETED.')
        os.environ['PO']=str(pod)
        os.environ['NS']=str(ns)
        os.system("kubectl delete pod $PO --namespace=$NS --grace-period=0 --force ")
