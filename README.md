# IliasAbgabenManager

## "Installation":
1. Alle Dateien in einen Ordner packen.
2. In diesem Ordner eine Datei namens "config" anlegen mit folgendem Inhalt:


        {
            "username":"<u-Kürzel>",
            "password":"<password>",
            "tries":2,
            "tutNr":<tut-nr>
            "course":948986
        }

## "How to use"
1. Mit der Konsole in den Ordner gehen
2. Manager.py mit python starten ("python Manager.py")
Dannach erscheint eine eigene Konsole in die die Weiteren Befehle eingegeben werden

## Commands:

- "**listTasks**": Auflistung aller bekannten Tasks/Übungsblätter
  - "-r" bzw. "--reload": Liste verfügbarer Tasks mit dem Ilias abgleichen
- "**getTask \<Übungsblatt ID\>**" Läd Abgaben zu entsprechendem Task herunter
  - "-y" bzw. "--yes": Vermute "Ja" als Antwort auf Nachfragen
- "**listSubmits \<Übungsblatt ID\>**" Auflistung aller vorhandenen Abgaben zu entsprechender Übung
- "**reduce \<Übungsblatt ID\> -w/-b \<u-Kürzel mit Komma getrennt\>**" Löscht alle Abgaben zu entsprechendem Übungsblatt, die auf der Blacklist(-b) oder nicht auf der Whitelist (-w) stehen.
- "**fetch \<Übungsblatt ID\> \<?Kürzel/ID\>**" Läd Abgabe des entsprechenden Studenten zu entsprechendem Übungsblatt in den workplace-Ordner. Wenn kein Studentfestgelegt wird nimmt es eine unabgeschlossene Abgabe .
- "**next \<punk1\> \<punkte2\> ...**" Nimmt die Abgabe aus dem workplace-Ordner, vermerkt die übergebenen Punkte als Bewertung für diese Person und kopiert (soweit vorhanden) eine neue Abgabe in den workplace-Ordner
- "**push \<Übungsblatt ID\> \<?Blattnummer\>**" Läd alle abgeschlossenen Abgaben als Rückmeldung in das Ilias hoch und trägt alle Punkte ins System ein (WICHTIG: Die Blattnummer sollte angegeben werden, für das Noten-System)
  - "-y" bzw. "--yes": Vermute "Ja" als Antwort auf Nachfragen
- "**backUpGrades**" Läd ein Backup der Punkte herunter, für den Fall, dass was schief laufen sollte

Nicht vollständig getestet:
- "**shelve \<?Übungsblatt ID\> \<?Kürzel\>**" Entfernt Abgabe(n) aus workplace-Ornder, markiert sie aber NICHT als (fertig) korrigiert.
  - "-a" bzw. "--all": shelves all
- "**points \<punk1\> \<punkte2\>**" Vermerkt angegebene Punkte für Abgabe,die aktuell im workplace-Ornder liegt
- "**commit \<?Übungsblatt ID\> \<?Kürzel\>**" Entfernt Abgabe(n) aus workplace-Ornder und markiert sie  als (fertig) korrigiert.
  - "-a" bzw. "--all": commits all


Weiter Funktionen existieren schon und kommen noch und werden wenn mal Zeit ist auber erklärt und weiter implementiert

## Gewöhnlicher Ablauf:


    listTasks -r 


(Es listet die vorhandenen Übungsblätter auf)

    getTask 27497 -r -y

(Alle Abgaben zu Blatt 4 werden heruntergeladen)

    reduce 27497 -w uzuse,ufjed,ufldf 

(Alle Abgaben, bis auf diese 3 werden gelöscht)

    listSubmits 27497 

(Listet jetzt nur noch die gewünschten Abgaben auf)

    fetch 27497 

(Läd die erst Abgabe. Diese wird korrigiert UND GESPEICHERT)

    next 3.5 4 

(Zuvor bearbeitete Abgabe wird mit 3.5 und 4 Punkten bewertet und aus dem workplace genommen. Eine neue Abgabe wird automatisch geladen)

    next 5.5 6 

usw bis eine Meldung kommt, dass alle Abgaben bearbeitet sind

    push 27497 4 

(Läd alle korrigierten Abgaben hoch und trägt die Punkte für Blatt 4 ein)
