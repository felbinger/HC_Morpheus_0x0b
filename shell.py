#!/usr/bin/python

import socket, sys, random, gnupg, os, json
from mysql import MySQL
from socket import error
from threading import Thread

config = json.loads(open("config.json").read())
path = config["shell"]["gpgdir"]
port = config["shell"]["port"]

gpg = gnupg.GPG(homedir=path)
connection_data = (config["db"]["host"], config["db"]["port"], config["db"]["user"], config["db"]["pass"], config["db"]["name"], config["db"]["charset"])

def client_handler(connection, fingerprint):
    try:
        code = random.randrange(0, 999999999999999)
        # print(code) # DEBUG
        connection.send(b"\033[1mItrago WebTool Emergency Access Shell\033[0m\nPlease decrypt the following message to verify that you are the Administrator (itragoadmin@hc.the-morpheus.de)!\n")
        connection.send(bytes("Encrypted Message:\n%s\n" % str(gpg.encrypt(str(code), fingerprint)),'utf-8'))
        connection.send(b"Message: ")
        if code == int(str(connection.recv(8192).decode('utf-8')).strip('\r').strip('\n')):
            connection.send(b"\n\033[1mEmergency Shell Access Granted\033[0m\n")
            while True:
                try:
                    connection.send(b"$ ")
                    data = str(connection.recv(8192).decode('utf-8')).strip('\r').strip('\n').strip()
                    if data == "exit" or data == "quit":
                        connection.close()
                        break;
                    elif data == "copyright":
                        connection.send(b"\033[1mCopyright\033[0m\n")
                        connection.send(b"Tim Supelir Intrago Company XY Consultment\n")
                    elif data == "help":
                        connection.send(b"\033[1mHelppage\033[0m\n")
                        connection.send(b"<SQL Query>   - Execute an SQL query\n")
                        connection.send(b"exit          - Quit the emergency shell\n")
                        connection.send(b"quit          - Quit the emergency shell\n")
                        connection.send(b"copyright     - Show the copyright informations\n")
                        connection.send(b"help          - Show this helppage\n")
                    else:
                        db = MySQL(*connection_data)
                        if data.upper().startswith("INSERT INTO"):
                            try:
                                rid = db.update(data)
                                connection.send(bytes("Okay, last inserted id: %s\n" % str(rid), 'utf-8'))
                            except Exception as e:
                                connection.send(
                                bytes(data + ": sql error\n",'utf-8'))
                        elif data.upper().startswith("SELECT") or data.upper().startswith("SHOW TABLES"):
                            try:
                                connection.send(bytes(str(db.queryAll(data)) + "\n", 'utf-8')) # convert to bytes
                            except Exception as e:
                                connection.send(bytes(data + ": sql error\n", 'utf-8'))
                        else:
                            connection.send(bytes(data + ": command not found\n", 'utf-8'))
                except ValueError:
                    connection.send(b"\n")
                    connection.close()
        else:
            connection.send(b"Access Denied\n")
            connection.close()
    except ValueError:
        connection.send(b"\n")
        connection.close()
    except BrokenPipeError:
        connection.send(b"\n")
        connection.close()

if __name__ == "__main__":
    try:
        if not os.path.exists(path + "/keyfile.asc"):
            data={'key_type': 'RSA',
                  'key_length': 2048,
                  'key_usage': 'ESCA',
                  'name_email': 'itragoadmin@hc.the-morpheus.de',
                  'passphrase': ''}
            key = gpg.gen_key(gpg.gen_key_input(**data))
            # Export key to key.txt
            with open(path + '/key.txt','w') as fw:
                fw.write(str(key.fingerprint))
            # Export Keys to keyfile.asc, on restart the app use the keys from the file
            with open(path + '/keyfile.asc','w') as f:
                f.write(gpg.export_keys(key))
                f.write(gpg.export_keys(key, True))
            print("New GPG Keys have been created!")
        fingerprint = open(path + "/key.txt", 'r').read()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', port))
            s.listen(3)
            print("Itrago Emergencs Shell has been started on port: " + str(port))
            while True:
                connection, addr = s.accept()
                new_client=Thread(target=client_handler, args=(connection,fingerprint))
                new_client.start()
            connection.close()
        except error:
            print("Unable to start Itrago Emergency Shell!")
    except KeyboardInterrupt:
        sys.exit(0)
