import csv
from FileHandling import file, exist

iliasPath = file('data','ilias-overview.csv')
mathPath = file('data','math-overview.csv')


iliasData = []
mathData = []
if exist(iliasPath):
    with open(iliasPath,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            iliasData.append(dict(row))
#print(iliasData)

if exist(mathPath):
    with open(mathPath,'r',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        tut = 1
        for row in reader:
            element = dict(row)
            if not len(mathData)==0:
                if element['Matrikelnummer']>mathData[-1]['Matrikelnummer']:
                    tut+=1
            element['Tut'] = tut
            mathData.append(element)
#print(mathData)


for e in mathData:
    e['Matrikelnummer'] = str(e['Matrikelnummer'])

for e in iliasData:
    for i in mathData:
        if e['Nachname'] == i['Nachname']:
            if e['Vorname'] != i['Vorname']:
                print('Error',e,i)

            #print('Combine',e,i)
            i['iliasID'] = str(e['iliasID'])
            #if not 'uID' in e.keys():
            #    print('No u-ID',e)
            i['uID'] = e['uID']
            break
    else:
        #print('Add',e)
        mathData.append(e)


mathNachname = {e['Nachname']:e for e in mathData}
mathVorname = {e['Vorname']:e for e in mathData}
mathUID = {e['uID']:e for e in mathData if 'uID' in e.keys()}
mathIliasID = {e['iliasID']:e for e in mathData if 'iliasID' in e.keys()}
mathMatrikelnummer = {e['Matrikelnummer']:e for e in mathData if 'Matrikelnummer' in e.keys()}
mathTut = {e['Tut']:e for e in mathData if 'Tut' in e.keys()}
#print(mathData)
#print(mathIliasID)
del(mathData)
