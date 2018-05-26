# HC_Morpheus_0x0b
Story:
Die Firma Itrago gibt ihnen den Auftrag ein von ihnen genutzte WebTool auf Schwachstellen zu untersuchen.
Der Leiter der IT Abteilung verspricht ihnen Firmenanteile, wenn sie in der Lage sind auf Unternehmensrelevante Daten zuzugreifen.

Solution:
1. Analyse der WebSchnittstellen (http://84.200.109.239:8080)
  - Merke: Beim Login wird das Passwort base64 kodiert an die API übergeben
  - Schnittstelle /getInfos mit POST aufrufbar (hier bekommt man die PGP keys)
  - Anweisungen zum Zurücksetzen des Passwortes im "Reset Password Modal"
2. Port der "Itrago Emergency Shell" herausfinden (nmap)
3. mit Telnet/Netcat in die "Itrago Emergency Shell" gehen
4. Angezeigte Nachicht: "Please decrypt the following message to verify that you are the Administrator (itragoadmin@hc.the-morpheus.de)!"
  - API /getInfo (steht als in development in der index.html) ansprechen und darüber pgp keys erhalten
  - Auf PGP Server auf Private Key stoßen und diesen nutzen um Message zu entschlüsseln
    - Linux: (Anleitung: https://wiki.snowbytesolutions.com/index.php/PGP#Linux)
      - gpg --import privatekey.txt
      - gpg -d
        - Message
        - STRG + D
    - Online Tool (BrowserAddon oder so - kenne ich keins - gibt es aber mit sicherheit)
5. Mithilfe von SQL Befehlen einen User-Account anlegen. (UPDATE/DELETE) wird nicht angeboten - damit die Challenge nicht zerstört werden kann
  - SHA1 hash über ein SELECT Herausfinden
  - Neuen Passwort generieren: sha1(base64(password))
6. Login auf der Login-Seite
