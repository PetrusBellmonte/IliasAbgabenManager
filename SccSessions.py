import requests, html
import Config
__session = requests.Session()

def getMASession():
    if not(Config.hasKey('username') and Config.hasKey('password')):
        print('Config has no entry "username" or "password"')
        return
    global __session
    r = __session.get('https://ma-vv.math.kit.edu/sso/overview')
    if not 'idp.scc.kit.edu' in r.url:
        print('Already Logged in by default????')
        return __session
    print('Login to MA-Portal')
    if 'j_username' in r.text:
        data = {'j_username':Config.get('username'), 'j_password':Config.get('password'), '_eventId_proceed': ''}
        r = __session.post(r.url,data=data)
    data = {}
    cont = r.text
    cont = cont[cont.index('action="')+len('action="'):]
    u = html.unescape(cont[:cont.index('"')])
    while 'name="' in cont:
        cont = cont[cont.index('name="')+len('name="'):]
        n = html.unescape(cont[:cont.index('"')])
        cont = cont[cont.index('value="')+len('value="'):]
        data[n] = html.unescape(cont[:cont.index('"')])
    __session.post(u,data=data)
    return __session

def getIliasSession():
    global __session
    r = __session.get('https://ilias.studium.kit.edu/ilias.php?baseClass=ilPersonalDesktopGUI&cmd=jumpToSelectedItems')
    if 'ilPersonalDesktopGUI' in r.url:
        print('Already Logged in by default????')
        return __session
    print('Login in to Ilias')
    r = __session.post('https://ilias.studium.kit.edu/login.php?target=&client_id=produktiv&cmd=force_login&lang=de')
    cont = r.text
    cont = cont[cont.index('<form'):cont.index('</form')]
    cont = cont[cont.index('action="')+len('action="'):]
    u = 'https://ilias.studium.kit.edu' + html.unescape(cont[:cont.index('"')])
    data = {}
    while 'name="' in cont:
        cont = cont[cont.index('name="')+len('name="'):]
        n = html.unescape(cont[:cont.index('"')])
        cont = cont[cont.index('value="')+len('value="'):]
        data[n] = html.unescape(cont[:cont.index('"')])
    r = __session.post(u, data=data)
    if 'j_username' in r.text:
        data = {'j_username':Config.get('username'), 'j_password':Config.get('password'), '_eventId_proceed': ''}
        r = __session.post(r.url,data=data)
    data = {}
    cont = r.text
    cont = cont[cont.index('action="')+len('action="'):]
    u = html.unescape(cont[:cont.index('"')])
    while 'name="' in cont:
        cont = cont[cont.index('name="')+len('name="'):]
        n = html.unescape(cont[:cont.index('"')])
        cont = cont[cont.index('value="')+len('value="'):]
        data[n] = html.unescape(cont[:cont.index('"')])
    __session.post(u,data=data)
    return __session

def post(url, *args, **kwargs):
    return __session.post(url, *args,**kwargs)

def get(url, **kwargs):
    return __session.get(url, **kwargs)
