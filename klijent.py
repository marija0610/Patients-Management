from tkinter import *
import socket
import time
from datetime import date
import json
from tkinter import messagebox


prozorKlijent=Tk()
prozorKlijent.geometry("415x500")
prozorKlijent.title("PACIJENT")

frejm1 = Frame(prozorKlijent)
frejm1.grid(row=0, column=0)
lblId=Label(frejm1, text="ID: ")
lblId.grid(row=0, column=0, pady=(10,0))
lblIme = Label(frejm1, text="Ime: ")
lblIme.grid(row=1, column=0)
lblPrezime = Label(frejm1, text="Prezime: ")
lblPrezime.grid(row=2, column=0)
lblJMBG = Label(frejm1, text="JMBG: ")
lblJMBG.grid(row=3, column=0)
lblTelefon = Label(frejm1, text="Telefon: ")
lblTelefon.grid(row=4, column=0)
lblDijagnoza = Label(frejm1, text="Dijagnoza: ")
lblDijagnoza.grid(row=5, column=0)

varId=StringVar()
varIme=StringVar()
varPrezime=StringVar()
varJMBG=StringVar()
varTelefon=StringVar()
varDijagnoza=StringVar()

txtId = Entry(frejm1, width=30, textvariable=varId)
txtId.grid(row=0, column=1, padx=20, pady=(10,0))
txtIme = Entry(frejm1, width=30, textvariable=varIme)
txtIme.grid(row=1, column=1, padx=20)
txtPrezime = Entry(frejm1, width=30, textvariable=varPrezime)
txtPrezime.grid(row=2, column=1, padx=20)
txtJMBG = Entry(frejm1, width=30, textvariable=varJMBG)
txtJMBG.grid(row=3, column=1, padx=20)
txtTelefon = Entry(frejm1, width=30, textvariable=varTelefon)
txtTelefon.grid(row=4, column=1, padx=20)
txtDijagnoza = Entry(frejm1, width=30, textvariable=varDijagnoza)
txtDijagnoza.grid(row=5, column=1, padx=20, pady=(0,10))

def prikazBaze():
    lstPrikaz.delete(0,END)
    s1 = socket.socket()
    host1 = socket.gethostname()
    port1 = 12345
    s1.connect((host1, port1))
    s1.send("Pacijenti".encode())
    prijemJson = json.loads(s1.recv(5120).decode())
    print(prijemJson)
    for item in prijemJson:
        lstPrikaz.insert(END, item)
    s1.close()

def dodaj():
    s = socket.socket()
    host = socket.gethostname()
    port = 12346
    s.connect((host, port))
    id = varId.get().strip()
    ime = varIme.get().strip()
    prezime = varPrezime.get().strip()
    jmbg = varJMBG.get().strip()
    if len(jmbg)!=13:
        messagebox.showinfo("Poruka","JMBG mora da ima 13 cifara")
        txtJMBG.delete(0,END)
    if jmbg.isdigit()==False:
        messagebox.showinfo("Poruka","JMBG mora da sadrzi samo cifre.")
        txtJMBG.delete(0, END)
    jmbg = varJMBG.get().strip()
    telefon = varTelefon.get().strip()
    if (str(telefon).startswith('06') or str(telefon).startswith('011'))==False:
        messagebox.showinfo("Poruka", "Telefon mora poceti sa 06 ili 011")
        txtTelefon.delete(0,END)
    if(telefon.isdigit()==False):
        messagebox.showinfo("Poruka","Telefon mora sadrzati samo cifre")
        txtTelefon.delete(0, END)
    if (len(telefon)!=10 or len(telefon)!=9)==False:
        messagebox.showinfo("Poruka", "Telefon treba da ima 9 ili 10 cifara")
        txtTelefon.delete(0, END)
    telefon = varTelefon.get().strip()
    dijagnoza= varDijagnoza.get().strip()

    if id=="" or ime == "" or prezime == "" or jmbg == "" or telefon == "" or dijagnoza == "":
        messagebox.showinfo("Poruka","Potrebno je da unesete sve podatke")
    else:
        s.send("Dodaj".encode())
        time.sleep(0.2)
        s.send((varId.get()).encode())
        time.sleep(0.2)
        s.send((varIme.get()).encode())
        time.sleep(0.2)
        s.send((varPrezime.get()).encode())
        time.sleep(0.2)
        s.send((varJMBG.get()).encode())
        time.sleep(0.2)
        s.send((varTelefon.get()).encode())
        time.sleep(0.2)
        s.send((varDijagnoza.get()).encode())
        time.sleep(0.2)
        odgovor = s.recv(1024).decode()
        print(odgovor)
        messagebox.showinfo("Poruka", odgovor)
        lstPrikaz.delete(0,END)
        txtId.delete(0,END)
        txtIme.delete(0,END)
        txtPrezime.delete(0, END)
        txtJMBG.delete(0, END)
        txtTelefon.delete(0, END)
        txtDijagnoza.delete(0, END)
    s.close()


# def izmeni():
    # s = socket.socket()
    # host = socket.gethostname()
    # port = 12347
    # s.connect((host, port))
    # s.send("Izmeni pacijenta".encode())
    # d = json.loads(s.recv(5120).decode())
    # lista = []
    # for item in d:
    #     lista.insert(END, item)
    #     txtId.insert(0,item[2])
    # s.close()
    #
    # idOznacenog=lstPrikaz.get(ACTIVE)[0]


def otpusti():
    s = socket.socket()
    host = socket.gethostname()
    port = 12348
    s.connect((host, port))
    id = varId.get().strip()
    if id == "":
        messagebox.showerror("Poruka", "Potrebno je da unesete id pacijenta.")
    else:
        s.send("Otpusti".encode())
        time.sleep(0.2)
        s.send((varId.get()).encode())
        time.sleep(0.2)
        odgovor = s.recv(1024).decode()
        print(odgovor)
        # lstPrikaz.insert(END, odgovor)
        messagebox.showinfo("Poruka",odgovor)
    s.close()
    lstPrikaz.delete(0,END)
    lstPrikaz.delete(0, END)
    txtId.delete(0, END)
    txtIme.delete(0, END)
    txtPrezime.delete(0, END)
    txtJMBG.delete(0, END)
    txtTelefon.delete(0, END)
    txtDijagnoza.delete(0, END)

frejm2=Frame(prozorKlijent, bg='lightgrey')
frejm2.grid(row=6, column=0)

btnPrikazBaze=Button(frejm2, text="Prikaz pacijenata", command=prikazBaze, bg='lightblue')
btnPrikazBaze.grid(row=6, column=0, padx=5, pady=5, ipadx=15)

btnDodaj=Button(frejm2, text="Dodaj pacijenta",command=dodaj, bg='lightblue')
btnDodaj.grid(row=6, column=1, padx=5, pady=5,ipadx=15)

# btnIzmeni=Button(frejm2, text="Izmeni podatke",command=izmeni, bg='lightblue')
# btnIzmeni.grid(row=6, column=2, padx=5, pady=5)

btnOtpusti=Button(frejm2, text="Otpusti pacijenta",command=otpusti, bg='lightblue')
btnOtpusti.grid(row=6, column=2, padx=5, pady=5,ipadx=15)

frejm3=Frame(prozorKlijent)
frejm3.grid(row=7, column=0)
scrollbar = Scrollbar(frejm3, orient="horizontal")
scrollbar.grid(row=9, column=0, columnspan=4, pady=5)
lstPrikaz= Listbox(frejm3, width=68, height=15)
lstPrikaz.grid(row=8, column=0, columnspan=4, pady=5)

lstPrikaz.config(xscrollcommand=scrollbar.set)
scrollbar.config(command=lstPrikaz.xview)

vreme1 = ''
lblTrenutnoVreme = Label(frejm3, font=('arial', 12, 'bold'), fg='blue', bg='lightgrey')
lblTrenutnoVreme.grid(row=10, column=1)

def tick():
    global vreme1
    vreme2 = time.strftime('%H:%M:%S')

    if vreme2 != vreme1:  # ukoliko se vreme promenilo, azurira ga
        time1 = vreme2
        lblTrenutnoVreme.config(text="Vreme: " + vreme2)
    lblTrenutnoVreme.after(20,tick)

tick()

danas=date.today()
datum=danas.strftime("%d/%m/%Y")


lblDatum= Label(frejm3, text="Datum: "+str(datum), font=('arial', 12, 'bold'), fg='blue', bg='lightgrey')
lblDatum.grid(row=10, column=0, padx=25)

prozorKlijent.mainloop()