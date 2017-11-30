import json
import os
import requests
import json
import os
import requests
import re

#get nodes list from heapster
def get_nodes(srv):
    url = 'http://' + srv + ':8082/api/v1/model/nodes'
    os.environ['URL']=str(url)
    os.system("curl -s $URL |sed '1d;$d' > /tmp/node.t")
    list = []
    for line in open("/tmp/node.t"):
        pattern = re.compile('"(.*)"')
        gt = pattern.findall(line)
        if gt != []:
            list += gt
    return list

#get value from dict type of heapster
def get_val(dict_1):
    if isinstance(dict_1, dict):
        tmpvalue = dict_1["metrics"][-1]
        return int(tmpvalue['value'])

#cluster mem used, total is memory/node_capacity
def mem_used(srv, nodes):
    sum = 0
    for node in nodes:
        url = 'http://' + srv + ':8082/api/v1/model/nodes/' + node + '/metrics/memory/usage'
        content = requests.get(url).content
        dic = eval(content)
        sum += get_val(dic)
    print sum
    return sum

#cluster mem working_set, total is memory/node_allocatable
def mem_hot(srv, nodes):
    sum = 0
    for node in nodes:
        url = 'http://' + srv + ':8082/api/v1/model/nodes/' + node + '/metrics/memory/working_set'
        content = requests.get(url).content
        dic = eval(content)
        sum += get_val(dic)
    print sum
    return sum

#calculate percent of mem_used
def use_per(nodes, usedmem):
    count = len(nodes)
    fullmem = float(count * 16658153472)
    pr = float(usedmem/fullmem)
    useper = format(pr, '0.2%')
    print "used percent is:",
    print useper
    return useper

#calculate percent of mem_hot
def hot_per(nodes, hotmem):
    count = len(nodes)
    fullmem = float(count * 15085289472)
    hotper = format(hotmem/fullmem, '0.2%')
    print "hot percent is:",
    print hotper
    return hotper

if __name__ == "__main__":
#replace ip to domain name in pod
    ip = '172.31.6.6'
    nodes = get_nodes(ip)
    used = mem_used(ip, nodes)
    hot = mem_hot(ip, nodes)
    up = use_per(nodes, used)
    hp = hot_per(nodes, hot)
