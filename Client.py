class Client:
    def __init__(self, buget, lista_de_produse):
        self.buget = buget
        self.lista_de_produse = dict(lista_de_produse)

    def plateste(self, de_achitat):#de_achitat poate fi buget or buget ramas, dupa primul apel al functiei in for
        a = self.lista_de_produse[(key)] * produse.pret[produse.nume.index(key)]
        cantitate = self.lista_de_produse[(key)]

        while a>de_achitat:
            cantitate=cantitate-1
            a=cantitate*produse.pret[produse.nume.index(key)]
        return a
