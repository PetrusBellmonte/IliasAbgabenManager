import SccSessions as Login
from FileHandling import file
import datetime

#hunchentoot-session=784:D99DA311991F50963AE2FFEE1AE28C6C; _shibsession_64656661756c7468747470733a2f2f6d612d76762e6d6174682e6b69742e6564752f7370=_64ec599487d49fccb780a8526148c0d6
import Config as conf
MAurl = 'https://ma-vv.math.kit.edu/sso/administrate-exercises'
indexUrl ='https://ma-vv.math.kit.edu/sso/index.html'
selectUrl = 'https://ma-vv.math.kit.edu/sso/select'
statusUrl = 'https://ma-vv.math.kit.edu/sso/tutor-status'
overviewUrl = 'https://ma-vv.math.kit.edu/sso/overview'

def post(url, *args, **kvargs):
    i= conf.conf['tries']
    while i >=0:
        r = Login.maS.post(url,*args, **kvargs)
        if not 'idp.scc.kit.edu' in r.url:
            return r
        Login.getMASession()
        i -= 1

def get(url, *args, **kvargs):
    i= conf.conf['tries']
    while i >=0:
        r = Login.maS.get(url,*args, **kvargs)
        if not 'idp.scc.kit.edu' in r.url:
            return r
        Login.getMASession()
        i -= 1

def setBlatt(nr,matr, points):
    prep()
    sheetData = {'sheet': nr, 'setsheet': 1}
    r = post(MAurl,data=sheetData)
    if not 'value="'+str(nr)+'"' in r.text:
        print('Failed to select Sheet',nr); return
    studentData = {'regnr':matr,'what':'Matrikelnummer','search':'Suche'}
    r = post(MAurl,data=studentData)
    if not 'value="'+str(matr)+'"' in r.text:
        print('Failed to select Matr',matr); return
    pointData = {'results['+str(i)+"]":points[i] for i in range(len(points))}
    pointData['setresults']=1
    r = post(MAurl,data=pointData)
    if not all('value="' + str(p) + '"' in r.text for p in points):
        print('Failed to push points', matr,points)

def setBlätter(nr,results):
    global cookies
    prep()
    sheetData = {'sheet': nr, 'setsheet': 1}
    r = post(MAurl,data=sheetData)
    if not 'value="'+str(nr)+'"' in r.text:
        print('Failed to select Sheet',nr); return
    for matr,points in results:
        studentData = {'regnr':matr,'what':'Matrikelnummer','search':'Suche'}
        r = post(MAurl,data=studentData)
        if not 'value="' + str(matr) + '"' in r.text:
            print('Skipping Matr', matr); continue
        pointData = {'results['+str(i)+"]":points[i] for i in range(len(points))}
        pointData['setresults']=1
        r = post(MAurl,data=pointData)
        if not all('value="' + str(p) + '"' in r.text for p in points):
            print('Failed to push points', matr,points)

def backUp():
    prep(overviewUrl)
    data = {
        'lname':'on',
        'fname':'on',
        'uid':'on',
        'exercises':'on',
        'total-score':'on',
        'sort1':'Tutorium',
        'sort2':'Matrikelnummer',
        'sort3':'Matrikelnummer',
        'csv':'CSV anfordern'
    }
    r = post(overviewUrl, stream=True, data=data)
    out = file('data', 'downloads', 'overview ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.csv')
    with open(out, 'wb') as handle:
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                handle.write(chunk)

def getStudentsOverView(f= file('data','math-overview.csv')):
    print('Collecting Student-Data from Grade-Portal')
    prep(overviewUrl)
    data = {
        'lname': 'on',
        'fname': 'on',
        'uid': 'on',
        'sort1': 'Tutorium',
        'sort2': 'Matrikelnummer',
        'sort3': 'Matrikelnummer',
        'csv': 'CSV anfordern'
    }
    r = post(overviewUrl, stream=True, data=data)
    with open(f, 'wb') as handle:
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                handle.write(chunk)

def prep(finalUrl = MAurl):
    r = get(selectUrl)
    if selectUrl == r.url:
        selectData = {'institute-name': 'Institut für Angewandte und Numerische Mathematik',
                      'semester': 'SS 2019', 'id': 210, 'submit': 'Vorlesung wählen'}
        r = post(selectUrl,data=selectData)
    if statusUrl == r.url:
        r = get(finalUrl)

#getStudentsOverView()
#setBlätter(2,[(2164692,[2,6]),(2261592,[4.5,3.5]),(2246328,[5,4.5]),(2260908,[5,6])])