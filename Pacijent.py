class Pacijent:
    def __init__(self, id, ime, prezime, jmbg, telefon, dijagnoza):
        self.id = id
        self.ime = ime
        self.prezime = prezime
        self.jmbg=jmbg
        self.telefon=telefon
        self.dijagnoza=dijagnoza

    def __str__(self):
        return str(self.id) + ". Ime: "+ str(self.ime) + " Prezime: " + str(self.prezime) + " JMBG: "+ str(self.jmbg) + " Telefon: "+ str(self.telefon) + " Dijagnoza: "+ str(self.dijagnoza)