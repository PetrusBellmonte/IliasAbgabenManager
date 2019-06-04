from FileHandling import *
import IliasAdapter, MaAdapter
import os, json, shutil

command = ''

FINISHED = 'finished'
PROGRESS = 'progress'

if not exist(file('workplace')):
    os.mkdir(file('workplace'))
if not exist(file('data')):
    os.mkdir(file('data'))
if not exist(file('data', 'downloads')):
    os.mkdir(file('data', 'downloads'))
if not exist(file('data', 'ilias-overview.csv')):
    IliasAdapter.getStudentsOverView()
if not exist(file('data', 'math-overview.csv')):
    MaAdapter.getStudentsOverView()

import StudentData as studData


def load(ubID, stud):
    print('Loading Task %s by %s %s (%s)' % (ubID, stud['Vorname'], stud['Nachname'], stud['iliasID']))
    homef = studFolder(ubID, stud)
    stfiles = [f for f in listDirWithFile(homef) if not f[0].endswith('points')]
    if any(f[0].split('.')[-2] == FINISHED for f in stfiles):
        stfiles = [f for f in stfiles if f[0].split('.')[-2] == FINISHED]
    elif any(f[0].split('.')[-2] == PROGRESS for f in stfiles):
        stfiles = [f for f in stfiles if f[0].split('.')[-2] == PROGRESS]
    for fn, f in stfiles:
        shutil.copy(f,
                    file('workplace', progFile(fn.replace('.' + FINISHED, '').replace('.' + PROGRESS, ''), ubID, stud)))


def unload(ubID, stud, status):
    success = False
    for fn, f in listDirWithFile(file('workplace')):
        sp = fn.split('.')
        if sp[-3] == ubID and sp[-2] == stud['iliasID']:
            shutil.copy(f, joinPath(studFolder(ubID, stud), ''.join(sp[:-5]) + '.' + status + '.' + sp[-1]))
            rmFile(f)
            success = True
    if not success:
        print('No File for %s by %s could be fount in the workplace' % (ubID, stud))


def onlyOneLoaded():
    ubID = None
    iliasID = None
    for f in listDir(file('workplace')):
        if (ubID is None or ubID == f.split('.')[-3]) or (iliasID is None or iliasID == f.split('.')[-2]):
            ubID = f.split('.')[-3]
            iliasID = f.split('.')[-2]
        else:
            print('Multiple Submissiond in workplace. Please choose one.')
            return None, None
    return ubID, iliasID


def nextStud(ubID):
    for d in listDir(ubFolder(ubID)):
        if not any([f.split('.')[-2] == FINISHED for f in listDir(d)]):
            return studData.byIliasID[folderStud(d)['iliasID']]
    print('Everything is already finished.')
    return


def savepoints(ubID, stud, points):
    folder = studFolder(ubID, stud)
    with open(joinPath(folder, '.points'), 'w') as f:
        f.write(json.dumps(points))


def getUbungen():
    ubs = []
    for f, d in listDirWithFile(file('data')):
        if f.startswith('ubungen'):
            ubs.append({'ubID': f.split('-')[-1], 'name': (f.split('-')[-2] if f.count('-') > 1 else 'unknown')})
    return ubs


def getStuds(ubID):
    studs = []
    for d in listDir(ubFolder(ubID)):
        if not any([f.split('.')[-2] == FINISHED for f in listDir(d)]):
            stts = 'f' if any([f.split('.')[-2] == FINISHED for f in listDir(d)]) else 'p' if any(
                [f.split('.')[-2] == PROGRESS for f in listDir(d)]) else '-'
            studs.append({**studData.byIliasID[folderStud(d)['iliasID']], 'status': stts})
    return studs


print('Ready!')
while True:
    print('> ', end='')
    command = input()
    if command.startswith('exit'):
        break

    if command.startswith('listTasks'):
        if '-r' in command or '--reload' in command:
            for u in IliasAdapter.getBlätter():
                fn = ubFolder(u[0])
                if not exist(fn):
                    os.mkdir(fn)
                if len(fn.split(os.pathsep)[-1].split('-')) == 2:
                    # TODO Teilt vor data
                    os.rename(fn, joinPath(*fn.split(os.pathsep)[:-1],
                                           fn.split(os.pathsep)[-1].replace('-', '-' + u[1] + '-')))
                pass
        ubs = getUbungen()
        if len(ubs) == 0:
            print('No tasks in the System. If there should be any, try "showTask -r"')
        else:
            print('ID\tName')
            for u in ubs:
                print(str(u['ubID']) + '\t' + u['name'])

    if command.startswith('getTask '):  # getTask <id> -y
        ubID = command.split(' ')[1]
        y = '-y' in command or '--yes' in command
        answer = ''
        if not y:
            print('Should it be downloaded? [y/n] ', end='')
            answer = input()
        if answer.lower() == 'y' or y:
            IliasAdapter.downloadAllesBlatt(ubID)

    if command.startswith('listSubmits '):  # list <ubID>
        ubID = command.split(' ')[1]
        if not exist(ubFolder(ubID)) or isEmpty(ubFolder(ubID)):
            print('No Task with this ID %s. Download it first with "getTask %s -r"' % (ubID, ubID))
        else:
            teams_list = ['MatrNr', 'Status', 'Last name', 'u-ID']
            data = [[s['Matrikelnummer'] if 'Matrikelnummer' in s.keys() else 'unknown', s['status'],
                     s['Nachname'], s['uID']] for s in getStuds(ubID)]
            row_format = "{:>15}" * (len(teams_list))
            print(row_format.format(*teams_list))
            for row in data:
                print(row_format.format(*row))

    if command.startswith('reduce '):  # reduce <ubID> -w/-b
        ubID = command.split(' ')[1]
        if not exist(ubFolder(ubID)):
            print('No Task with id', ubID)
            continue
        if ' -w ' in command:
            args = command.split(' ')
            l = args[args.index('-w') + 1].split(',')
            for f in listDir(ubFolder(ubID)):
                if not f.split('_')[-2] in l:
                    rmFile(f)
        elif ' -b ' in command:
            args = command.split(' ')
            l = args[args.index('-b') + 1].split(',')
            for f in listDir(ubFolder(ubID)):
                if f.split('_')[-2] in l:
                    rmFile(f)
        print('Done')

    if command.startswith('fetch '):  # fetch <ubID> <?iliasID/u-ID>
        ubID = command.split(' ')[1]
        if command.count(' ') >= 2:
            sid = command.split(' ')[2]
            if sid[0] == 'u' or sid[0] == 't':
                std = studData.byUID[sid]
            else:
                std = studData.byIliasID[sid]
        else:
            std = nextStud(ubID)
            if std is None:
                continue
        load(ubID, std)

    if command.startswith('shelve'):  # shelf <ubUD>
        if command.strip() == 'shelve':
            ubID, iliasID = onlyOneLoaded()
            print(ubID, iliasID)
            if not ubID is None:
                unload(ubID, studData.byIliasID[iliasID], PROGRESS)
                print('Shelved %s by %s' % (ubID, iliasID))
        elif '-a' in command or '--all' in command:
            tbr = set(tuple(f.split('.')[-3:-2]) for f in listDir(file('workplace')))
            for ubID, iliasID in tbr:
                unload(ubID, studData.byIliasID[iliasID], PROGRESS)
                print('Shelved %s by %s' % (ubID, iliasID))
        else:
            if len(command.split(' ')) < 3:
                print('Please specify Task and Studend: "shelve <taskID> <u-ID>"')
            ubID = command.split(' ')[1]
            uID = command.split(' ')[2]
            unload(ubID, studData.byUID[uID], PROGRESS)
            print('Shelved %s by %s' % (ubID, uID))

    if command.startswith('commit'):  ######################### DO NOT CHANGE THIS METHOD!!!!!!!!!!!!!!!!
        if command.strip() == 'commit':
            ubID, iliasID = onlyOneLoaded()
            if not ubID is None:
                unload(ubID, studData.byIliasID[iliasID], FINISHED)
                print('Committed %s by %s' % (ubID, iliasID))
        elif '-a' in command or '--all' in command:
            tbr = set(tuple(f.split('.')[-3:-2]) for f in listDir(file('workplace')))
            for ubID, iliasID in tbr:
                unload(ubID, studData.byIliasID[iliasID], FINISHED)
                print('Committed %s by %s' % (ubID, iliasID))
        else:
            if len(command.split(' ')) < 3:
                print('Please specify Task and student: "commit <taskID> <u-ID>"')
            ubID = command.split(' ')[1]
            uID = command.split(' ')[2]
            unload(ubID, studData.byUID[uID], FINISHED)
            print('Committed %s by %s' % (ubID, uID))

    if command.startswith('next'):
        ubID, iliasID = onlyOneLoaded()
        if ubID is None:
            continue
        unload(ubID, studData.byIliasID[iliasID], FINISHED)
        if len(command.split(' ')) > 1:
            points = [e for e in command.split(' ')[1:]]
            savepoints(ubID, studData.byIliasID[iliasID], points)
        std = nextStud(ubID)
        if std is None:
            continue
        load(ubID, std)

    if command.startswith('points'):
        ubID, iliasID = onlyOneLoaded()
        if ubID is None:
            print('There can only be one persons files in the workplace-folder to use this command!')
            continue
        points = [e for e in command.split(' ')[1:]]
        savepoints(ubID, studData.byIliasID[iliasID], points)
        print('Points saved')

    if command.startswith('push'):  # push <ubID> <nr>
        if ' ' not in command:
            print('Incorrect command-format: "push <Task-ID> <Number>"');
            continue
        ubID = command.split(' ')[1]
        y = '-y' in command or '--yes' in command

        if command.count(' ') == 2:
            nr = command.split(' ')[2]
        else:
            nr = ubFolder(ubID).split('-')[-2]
            if nr =='ubungen':
                print('Incorrect command-format: "push <Task-ID> <Number>"');
                continue
            answer = ''
            if not y:
                print('Should \"'+nr+'\" be the task-number? [y/n] ', end='')
                answer = input()
            if not answer.lower() == 'y' and not y:
                print('Incorrect command-format: "push <Task-ID> <Number>"');
                continue

        results = []
        for f in [fo for fo in listDir(ubFolder(ubID)) if
                  any(f2.split('.')[-2] == FINISHED for f2 in os.listdir(fo)) or exist(joinPath(fo, '.points'))]:
            stud = studData.byIliasID[f.split('_')[-1]]
            if not any('-feedback.' in f3 for f3 in os.listdir(f)):
                for ff in [f3 for f3 in listDir(f) if f3.split('.')[-2] == FINISHED]:
                    parts = ff.replace('.' + FINISHED, '').split('.')
                    ufn = '.'.join(parts[:-1]) + '-feedback.' + parts[-1]
                    shutil.copy(ff, ufn)
                    #IliasAdapter.upload(ubID, stud, ufn)

            if 'Matrikelnummer' in stud.keys() and exist(joinPath(f, '.points')):
                with open(joinPath(f, '.points'), 'r') as pf:
                    points = json.loads(''.join(pf.readlines()))
                    results.append((stud['Matrikelnummer'], tuple(points)))
        if not results == []:
            MaAdapter.setBlätter(nr, results)

    if command == 'backUpGrades':
        MaAdapter.backUp()

    if command.startswith('load'):
        pass