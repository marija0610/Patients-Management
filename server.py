import json
import socket
import sqlite3
import threading
import datetime
import functools
from tkinter import *
from Pacijent import Pacijent

prozorServer = Tk()
prozorServer.geometry("300x450")
prozorServer.title("SERVER")

lbServer = Listbox(prozorServer, width=60, height=40)
lbServer.pack(side=LEFT)


conn = sqlite3.connect('pacijenti.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS pacijenti(
        id INTEGER PRIMARY KEY,
        ime text,
        prezime text,
        jmbg text,
        telefon text,
        dijagnoza text
        )""")


sql = """SELECT count(*) FROM pacijenti"""


def posaljiBazu():
    s1 = socket.socket()
    host1 = socket.gethostname()
    port1= 12345
    s1.bind((host1, port1))
    s1.listen(5)

    global listaZaJson
    while True:
        konekcija, adresa = s1.accept()
        zahtev = konekcija.recv(1024).decode()
        now = datetime.datetime.now()
        if zahtev == "Pacijenti":
            lbServer.insert(END,"SERVER: Primljen zahtev za prikaz svih pacijenata")
            conn = sqlite3.connect('pacijenti.db')
            c = conn.cursor()
            c.execute("SELECT * FROM pacijenti")
            lpacijenti = c.fetchall()
            if sql==0:
                konekcija.send("Jos nema nijednog pacijenta ".encode())
                f = open("poruke.txt", "a")
                f.write("Server nije poslao klijentu spisak svih pacijenata, jer ne postoji nijedan u bazi. Datum: " + str(now.strftime('%d/%m/%Y')) + " \n")
                f.close()
                lbServer.insert(END, "SERVER: Primljen zahtev za prikaz svih pacijenata")
            else:
                listaPacijenata = []
                for p in lpacijenti:
                    listaPacijenata.append(Pacijent(str(p[0]), p[1], p[2], p[3], p[4], p[5]))

                listaZaJson = []
                for p in listaPacijenata:
                    listaZaJson.append(functools.reduce((lambda x, y: x + y), p.__str__()))

                pacijentiUJson = json.dumps(listaZaJson)
                konekcija.send(pacijentiUJson.encode())
                f = open("poruke.txt", "a")
                f.write("Server je poslao klijentu spisak svih pacijenata. Datum: " + str(now.strftime('%d/%m/%Y')) + " \n")
                f.close()
                lbServer.insert(END, "SERVER: Opsluzen zahtev za prikaz pacijenata.")
        konekcija.close()


def dodajPacijenta():
    s = socket.socket()
    host = socket.gethostname()
    port = 12346
    s.bind((host, port))
    s.listen(5)

    while True:
        konekcija1, adresa = s.accept()
        zahtev = konekcija1.recv(1024).decode()
        if zahtev == "Dodaj":
            lbServer.insert(END, "SERVER: Primljen zahtev za dodavanje pacijenta.")
            id = konekcija1.recv(1024).decode()
            ime = konekcija1.recv(1024).decode()
            prezime = konekcija1.recv(1024).decode()
            jmbg = konekcija1.recv(1024).decode()
            telefon = konekcija1.recv(1024).decode()
            dijagnoza = konekcija1.recv(1024).decode()
            now = datetime.datetime.now()

            try:
                conn = sqlite3.connect('pacijenti.db')
                c = conn.cursor()
                c.execute("INSERT INTO pacijenti VALUES(:id, :ime, :prezime, :jmbg, :telefon, :dijagnoza)",
                                {
                                    'id':id,
                                    'ime': ime,
                                    'prezime': prezime,
                                    'jmbg': jmbg,
                                    'telefon':telefon,
                                    'dijagnoza':dijagnoza
                                })
                conn.commit()
                conn.close()
                print("Pacijent je dodat.")
                konekcija1.send("Pacijent je dodat.".encode())
                f = open("poruke.txt", "a")
                f.write("Pacijent: " + ime +" "+ prezime+" sa dijagnozom:" +dijagnoza +" je dodat." +" Datum: " + str(now.strftime('%d/%m/%Y')) + " \n")
                f.close()
                lbServer.insert(END, "SERVER:Opsluzen zahtev za dodavanje pacijenta.")
                lbServer.insert(END, "Dodat pacijent: "+ime +" "+prezime)
            except:
                print("Doslo je do greske sa bazom.")
                konekcija1.send("Dogodila se greska sa bazom.".encode())
                lbServer.insert(END, "Opsluzen zahtev za dodavanje pacijenta.\n Dodat pacijent: " + ime + " " + prezime)
                f = open("poruke.txt", "a")
                f.write("Pokusano je dodavanje pacijenta. Desila se greska. " + " Datum: " + str(now.strftime('%d/%m/%Y')) + " \n")
                f.close()
                lbServer.insert(END, "SERVER: Nije uspelo dodavanje novog pacijenta")
                conn.rollback()

        konekcija1.close()
    s.close()

# def izmeniPodatke():
#     s = socket.socket()
#     host = socket.gethostname()
#     port = 12347
#     s.bind((host, port))
#     s.listen(5)
#
#     global lista2, conn4, conn2
#     konekcija,adresa=s.accept()
#     zahtev=konekcija.recv(1024).decode()
#     if zahtev=="Izmeni pacijenta":
#         while True:
#             konekcija1, adresa = s.accept()
#             podaci = json.dumps(lista2)
#             konekcija1.send(podaci.encode())
#
#     konekcija.close()

def otpustiPacijenta():
    s = socket.socket()
    host = socket.gethostname()
    port = 12348
    s.bind((host, port))
    s.listen(5)

    while True:
        konekcija, adresa = s.accept()
        zahtev = konekcija.recv(1024).decode()
        now = datetime.datetime.now()
        if zahtev == "Otpusti":
            lbServer.insert(END, "SERVER: Primljen zahtev za otpustanje pacijenta.")
            id = konekcija.recv(1024).decode()
            try:
                conn1 = sqlite3.connect('pacijenti.db')
                c1 = conn1.cursor()
                conn2 = sqlite3.connect('pacijenti.db')
                c2 = conn2.cursor()
                c2.execute("SELECT * FROM pacijenti")
                pacijenti=c2.fetchall()
                listaID=[]
                for p in pacijenti:
                    listaID.append((p[0], p[1],p[2],p[3], p[4], p[5]))
                primljeniID = id
                odabraniPac= list(filter(lambda x: x[0] == int(primljeniID), listaID))
                print(odabraniPac)
                lbServer.insert(END, "SERVER: Otpusten sledeci pacijent: ")
                lbServer.insert(END, odabraniPac)

                query = "DELETE FROM pacijenti WHERE id=?"
                c1.execute(query, id)
                conn2.commit()
                conn1.commit()
                conn2.close()
                conn1.close()
                print("Pacijent je otpusten.")
                konekcija.send("Uspesno ste otpustili pacijenta.".encode())
                f = open("poruke.txt", "a")
                f.write("Otpusten je pacijent: " + id + " Datum: " + str(
                    now.strftime('%d/%m/%Y')) + " \n")
                f.close()
            except:
                print("Doslo je do greske sa bazom.")
                konekcija.send("Dogodila se greska. Proverite da li ste uneli dobar id.".encode())
                lbServer.insert(END, "SERVER: Došlo je do greške..")
                f = open("poruke.txt", "a")
                f.write("Desila se greska usled pokušaja otpuštanja pacijenta" + " Datum: " + str(
                    now.strftime('%d/%m/%Y')) + " \n")
                f.close()
                conn1.rollback()
        konekcija.close()


nit = threading.Thread(target=posaljiBazu, args=()).start()
nit1 = threading.Thread(target=dodajPacijenta, args=()).start()
# nit2 = threading.Thread(target=izmeniPodatke, args=()).start()
nit3=threading.Thread(target=otpustiPacijenta, args=()).start()

prozorServer.mainloop()
