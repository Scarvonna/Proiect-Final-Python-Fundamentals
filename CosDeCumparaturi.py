class CosDeCumparaturi(Client):
    def __init__(self, lista_de_produse):#lista ce contine liste [[]] =[[produs, cantitatea]] care poate fi CUMPARATE:
                                         #exista in magazin si clientul are buget pentru ele
        self.lista_de_produse = lista_de_produse

    def adauga_produs(self, produs, cantitate):
        if cantitate>0:
            return f"{produs}.....x{cantitate}"
        else:
            return "\n"

    def elibereaza_bon(self):
        return "               Bon fiscal\n"
