import requests, html
import Config

maS = requests.Session()
def getMASession():
    if not(Config.hasKey('username') and Config.hasKey('password')):
        print('Config has no entry "username" or "password"')
        return
    global maS
    r = maS.get('https://ma-vv.math.kit.edu/sso/overview')
    if not 'idp.scc.kit.edu' in r.url:
        print('Already Logged in by default????')
        return maS
    print('Login to MA-Portal')
    data = {'j_username':Config.get('username'), 'j_password':Config.get('password'), '_eventId_proceed': ''}
    r = maS.post(r.url,data=data)
    data = {}
    cont = r.text
    cont = cont[cont.index('action="')+len('action="'):]
    u = html.unescape(cont[:cont.index('"')])
    while 'name="' in cont:
        cont = cont[cont.index('name="')+len('name="'):]
        n = html.unescape(cont[:cont.index('"')])
        cont = cont[cont.index('value="')+len('value="'):]
        data[n] = html.unescape(cont[:cont.index('"')])
    maS.post(u,data=data)
    return maS

iliasS = requests.Session()
def getIliasSession():
    global iliasS
    r = iliasS.get('https://ilias.studium.kit.edu/ilias.php?baseClass=ilPersonalDesktopGUI&cmd=jumpToSelectedItems')
    if 'ilPersonalDesktopGUI' in r.url:
        print('Already Logged in by default????')
        return iliasS
    print('Login in to Ilias')
    r = iliasS.post('https://ilias.studium.kit.edu/login.php?target=&client_id=produktiv&cmd=force_login&lang=de')
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
    r = iliasS.post(u, data=data)
    data = {'j_username':Config.get('username'), 'j_password':Config.get('password'), '_eventId_proceed': ''}
    r = iliasS.post(r.url,data=data)
    data = {}
    cont = r.text
    cont = cont[cont.index('action="')+len('action="'):]
    u = html.unescape(cont[:cont.index('"')])
    while 'name="' in cont:
        cont = cont[cont.index('name="')+len('name="'):]
        n = html.unescape(cont[:cont.index('"')])
        cont = cont[cont.index('value="')+len('value="'):]
        data[n] = html.unescape(cont[:cont.index('"')])
    r = iliasS.post(u,data=data)
    return iliasS
