import zipfile, os

file = lambda *path: os.path.join(os.path.dirname(os.path.abspath(__file__)), *path)
joinPath = lambda *s: os.path.join(*s)
exist = lambda f: os.path.exists(f)

def isEmpty(f):
    for f2 in os.listdir(f):
        print(f2)
        return False
    return True


def ubFolder(ubID):
    for f in os.listdir(file('data')):
        if f.endswith(ubID):
            return joinPath('data', f)
    return file('data', 'ubungen-' + ubID)

def progFile(f,ubID,stud):
    return '.'.join(['.'.join(f.split('.')[:-1]),stud['Vorname'],stud['Nachname'],ubID,stud['iliasID']+'.'+f.split('.')[-1]])

def studFolder(ubID, stud):
    for f in os.listdir(ubFolder(ubID)):
        if f.endswith(stud['iliasID']):
            return joinPath(ubFolder(ubID), f)
    return joinPath(ubFolder(ubID), '_'.join([stud['Nachname'],stud['Vorname'],stud['uID'],stud['iliasID']]))

def folderStud(f):
    sep = f.split(os.pathsep)[-1].split('_')
    return {'Nachname':sep[0],'Vorname':sep[1],'uID':sep[2],'iliasID':sep[3]}

def unzip(zipPath, outPath):
    print('Unzipping files....', end='\r')
    zip_ref = zipfile.ZipFile(zipPath, 'r')
    zip_ref.extractall(outPath)
    zip_ref.close()
    print('Unzipping finished')

def listDir(d):
    for f in os.listdir(d):
        yield joinPath(d,f)
def listDirWithFile(d):
    for f in os.listdir(d):
        yield f, joinPath(d,f)

def rmFile(f):
    if os.path.isdir(f):
        for ff in listDir(f):
            rmFile(ff)
        os.rmdir(f)
    else:
        os.remove(f)


