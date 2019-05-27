import json, sys, os

__conf = {}
file = lambda *path: os.path.join(os.path.dirname(os.path.abspath(__file__)), *path)


def reload():
    global __conf
    with open(file('config')) as f:
        __conf = json.loads(''.join(f.readlines()))


def save():
    global __conf
    with open(file('config'), 'w') as f:
        f.write(json.dumps(__conf))

reload()



def get(key, default=None):
    return __conf[key] if key in __conf.keys() else default

def hasKey(key):
    return key in __conf

# Defaults
username = __conf['username']
password = __conf['password']

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        if args[0] == 'reload':
            reload()
        elif args[0] == 'set':
            if len(args) == 3:
                __conf[args[1]] = args[2]
                save()
