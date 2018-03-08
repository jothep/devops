#on k8s master
#scale replicas number by namespace

import os
import sys, getopt


def repl(ns,replica):
    cmd = "kubectl get deploy --no-headers -n " + ns + " |awk '{print $1}'"
    ret = os.popen(cmd).read()
    list1 = []
    if ret != "":
        list1 = ret.split('\n')[:-1]
    else:
        print("no deploy here")
        sys.exit()
    for i in list1:
        cmd_rep = "kubectl scale --replicas=" + str(replica) +' '+'deploy/'+i+' -n'+' '+ns
        os.popen(cmd_rep).read()
    print("scale done")

def main(argv):
    namespace = ""
    replicas = 0

    try:
        opts, args = getopt.getopt(argv, "hn:r:",["namespace=", "replicas="])
    except getopt.GetoptError:
        print('Error: -n <namespace> -r <replicas>')
        print('    or: --namespace=<namespace> --replicas=<replicas>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print('Error: -n <namespace> -r <replicas>')
            print('    or: --namespace=<namespace> --replicas=<replicas>')
            sys.exit()
        elif opt in ("-n", "--namespace"):
            namespace = arg
        elif opt in ("-r", "--replicas"):
            replicas = arg

    if namespace != "":
        repl(namespace, replicas)
    else:
        print('Error: -n <namespace> -r <replicas>')
        print('    or: --namespace=<namespace> --replicas=<replicas>')

if __name__ == "__main__":
    main(sys.argv[1:])
