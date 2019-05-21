# IliasAbgabenManager

"Installation":
1. Alle Dateien in einen Ordner packen.
2. In diesem Ordner eine Datei namend "config" anlegen mit folgendem Inhalt:

{
    "username":"<u-Kürzel>",
    "password":"<password>",
    "tries":2,
    "tutNr":<tut-nr>}

"How to use"
1. Mit der Konsole in den Ordner gehen
2. Manager.py mit python starten ("python Manager.py")
Dannach erscheint eine eigene Konsole in die die Weiteren Befehle eingegeben werden

Commands:
- "listTasks": Auflistung aller bekannten Tasks/Übungsblätter
- "listTasks -r": vgl oben, nur dass es sich mögliche neue Blätter aus dem Ilias hohlt
- "getTask \<iliasID\> -r" downloaden des Übungsblattes mit entsprechender iliasID (bei listTasks zu finden)
- "listSubmits \<iliasID\>" Auflistung aller vorhandenen Abgaben zu der Übung mit entsprechender iliasID
- "fetch \<iliasID\>" Kopiert einer unabgeschlossene Abgabe zu entsprechendem Übungsblatt in den workplaceordner
- "reduce \<iliasID\> -w/-b \<u-Kürzel mit komme getrennt\>" Löschte alle Abgeben zu entsprechendem Übungsblatt die nicht auf der Whitelist (-w) oder auf der blacklist(-b) stehen.
- "next \<punk1\> \<punkte2\> ..." Kopiert die Abgabe aud dem Workplace-ordner weg, merkt sich die übergebenen Punkte als bewertung für diese Peron und kopiert (soweit vorhanden) eine neue Abgabe in den workplace-ordner
- "push \<iliasID\> \<Blattnummer\> Läd alle korrigierten Abgaben ins ilias hoch und trägt alle Punkte ins System ein (WICHTIG: Die Blattnummer muss angegeben werden, für das Noten-System)
- "backUpGrades" lad ein backup der Punkte runter, für den Fall, dass was schief laufen sollte

Weiter Funktionen existieren schon und kommen noch und werden wenn mal Zeit ist auber erklärt und weiter implementiert
