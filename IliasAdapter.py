import html, os

import SccSessions as Login
import Config as conf
from FileHandling import file, unzip, studFolder, joinPath,ubFolder

helpurl = "https://ilias.studium.kit.edu/templates/default/images/icon_exc.svg"
baseurl = "https://ilias.studium.kit.edu/"
feedbackurl = lambda ubID, stud: 'https://ilias.studium.kit.edu/ilias.php?ref_id=948986&ass_id=%s&vw=1&member_id=%s&cmd=listFiles&cmdClass=ilfilesystemgui&cmdNode=11k:11g:10w:jd&baseClass=ilExerciseHandlerGUI' % (ubID, stud['iliasID'])
desktop = 'https://ilias.studium.kit.edu/ilias.php?baseClass=ilPersonalDesktopGUI&cmd=jumpToSelectedItems'
overviewurl = 'https://ilias.studium.kit.edu/ilias.php?ref_id=948986&cmd=members&cmdClass=ilexercisemanagementgui&cmdNode=11k:11g:1&baseClass=ilExerciseHandlerGUI'
#overviewurl = "https://ilias.studium.kit.edu/ilias.php?ref_id=948986&vw=1&exc_mem_trows=800&cmd=members&cmdClass=ilexercisemanagementgui&cmdNode=11k:11g:10w&baseClass=ilExerciseHandlerGUI"
loginurl = "https://ilias.studium.kit.edu/login.php?target=&client_id=produktiv&cmd=force_login&lang=de"


def post(url, *args, **kvargs):
    i = conf.conf['tries']
    while i >= 0:
        r = Login.iliasS.post(url, *args, **kvargs)
        if not 'reloadpublic' in r.url:
            return r
        Login.getIliasSession()
        i -= 1


def get(url, *args, **kvargs):
    i = conf.conf['tries']
    while i >= 0:
        r = Login.iliasS.get(url, *args, **kvargs)
        if not 'reloadpublic' in r.url:
            return r
        Login.getIliasSession()
        i -= 1


def getBlätter():
    asss = []
    r = post(overviewurl)
    content = r.text
    i = content.index('id="ass_id"')
    content = content[i:content.index("</select>", i)]
    while 'option value="' in content:
        i = content.index('option value="') + len('option value="')
        id = html.unescape(content[i:content.index('"', i + 1)])
        i = content.index('>', i + 1) + 1
        asss.append((id, html.unescape(content[i:content.index('<', i + 1)])))
        content = content[i:]
    return asss

#https://ilias.studium.kit.edu/ilias.php?baseClass=ilExerciseHandlerGUI&ref_id=948986&cmd=showOverview
#https://ilias.studium.kit.edu/ilias.php?ref_id=948986&vw=1&exc_mem_trows=800&cmd=members&cmdClass=ilexercisemanagementgui&cmdNode=11k:11g:10w&baseClass=ilExerciseHandlerGUI
#https://ilias.studium.kit.edu/ilias.php?ref_id=948986&cmd=members&cmdClass=ilexercisemanagementgui&cmdNode=11k:11g:1&baseClass=ilExerciseHandlerGUI



def downloadAllesBlatt(ubID):
    r = get(overviewurl)
    datadic = {'ass_id': int(ubID), 'cmd[downloadAll]': 'Alle Abgaben herunterladen', 'user_login': ''}
    content = r.text
    i = content.index('id="ilToolbar"')
    i = content.index('action="', i + 1) + len('action="')
    url = baseurl + html.unescape(content[i:content.index('"', i + 1)])
    # r = post(url, stream=True, data=datadic)
    print('Requesting Data...', end='\r')
    r = post(url, stream=True, data=datadic)
    totalLen = int(r.headers.get('content-length'))
    print('Receiving Data...')
    out = file('data', 'downloads', 'ubungen-' + ubID + '.zip')
    with open(out, 'wb') as handle:
        dl = 0
        a = 0
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                dl += len(chunk)
                if not a == int(dl * 50 /int(totalLen)):
                    a = int(dl * 50 /int(totalLen))
                    if dl<=totalLen:
                        print('[' + '#' * a + ' ' * (50 - a) + ']' + str(dl) + '/' + str(totalLen), end='\r')
                handle.write(chunk)
    print('Finished Saving')
    unzip(out, ubFolder(ubID))


def downloadBlatt(ubID, stud):
    url = 'https://ilias.studium.kit.edu/ilias.php?ref_id=948986&vw=1&member_id=%s&ass_id=%s&cmd=downloadReturned&cmdClass=ilexsubmissionfilegui&cmdNode=11k:11g:10w:10q&baseClass=ilExerciseHandlerGUI' \
          % (str(stud['iliasID']), ubID)
    finalDir = studFolder(ubID, stud)
    r = get(url, stream=True)
    fn = str(r.headers['content-disposition'])
    fn = fn[fn.index('filename="') + len('filename="'):]
    fn = fn[:fn.index('"')]
    if fn.split('.')[-1] == 'zip':
        out = file('data', 'downloads')
    else:
        out = finalDir
    if not os.path.exists(finalDir):
        os.mkdir(finalDir)
    out = out + os.pathsep + fn
    with open(out, 'wb') as handle:
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                handle.write(chunk)
    if fn.split('.')[-1] == 'zip':
        unzip(out, file('data', 'ubungen-' + ubID,
                        stud['Nachname'] + '_' + stud['Vorname'] + '_' + stud['Kürzel'] + '_' + stud['iliasID']))


def upload(ubID, stud,f):
    print(' Upload %s by %s %s (%s) to Task %s'%(f.split(os.sep)[-1], stud['Vorname'], stud['Nachname'],stud['uID'], ubID))
    r = get(feedbackurl(ubID, stud))
    cont = r.text
    cont = cont[cont.index('"ilToolbar"'):]
    cont = cont[cont.index('action="') + len('action="'):]
    url = baseurl + html.unescape(cont[:cont.index('"')])
    files = {'new_file': open(f, 'rb')}
    r = post(url, files=files, data={'cmd[uploadFile]': 'Hochladen'})

def getStudentsOverView(f=file('data', 'ilias-overview.csv')):
    with open(f, 'w') as f:
        f.write('iliasID,Nachname,Vorname,uID\n')
        r = get(overviewurl)
        cont = r.text
        while 'tblrow' in cont:
            cont = cont[cont.index('tblrow'):]
            cont = cont[cont.index('member[') + len('member['):]
            line = html.unescape(cont[:cont.index(']')]) + ','
            cont = cont[cont.index('<td') + len('<td'):]
            line += html.unescape(cont[cont.index('>') + 1:cont.index('<')].replace(', ', ',').replace('\n', '').strip()) + ','
            cont = cont[cont.index('<td') + len('<td'):]
            f.write(line + html.unescape(cont[cont.index('>') + 1:cont.index('<')].strip()) + '\n')


