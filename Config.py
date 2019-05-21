import json, sys, os

conf = {}
file = lambda *path: os.path.join(os.path.dirname(os.path.abspath(__file__)), *path)

def reload():
    global conf
    with open(file('config')) as f:
        conf = json.loads(''.join(f.readlines()))

reload()
#print(conf)

#Defaults
username = conf['username']
password = conf['password']

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args)>0:
        if args[0] == 'reload':
            reload()
        elif args[0] == 'set':
            if len(args) == 3:
                conf[args[1]] = args[2]
