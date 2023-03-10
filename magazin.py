import os
import sys
import Produs
import Client
import CosDeCumparaturi


#crearea stocului magazinului
produse = Produs([], [], [])
with open(sys.argv[1], mode='r') as f:  #context manager
    for x in f.readlines():
        a, b, c = x.partition(",")  #partition imparte stringul intr-o tupla cu 3 elemente ex:
        d, e, f = c.partition(",")  #a=paine, b=",",c=50,3
        produse.nume.append(a), produse.stoc.append(int(d)), produse.pret.append(int(f.strip("\n")))
        # print(produse.nume, produse.stoc, produse.pret)

#accesarea fisierelor text din folder
os.chdir(sys.argv[2])
lista = os.listdir(os.chdir(sys.argv[2]))  #lista cu "nume.txt" a fisierelor din folder

a = str()
key = []
value = []
cos=CosDeCumparaturi([])

#listele de cumparaturi si bugetul clientilor
for i in lista:
    client = Client(int(), {})#i=fisier cu info despre fiecare client in parte
                              #atributele obiectului client trebuie initiate cu "0" pentru fiecare client in parte
    with open(i, mode='r') as o:
        k = o.readlines()

        client.buget = int(k[0])#primul element din lista
        #print(client.buget)

        for a in k[1:]:#celelalte elemente din lista
            key, b, value = a.partition(",")
            client.lista_de_produse.update({key: int(value.strip("\n"))})
    #print(client.lista_de_produse)
    #print(client.buget)

    subtotal=0
    total=0

    #generarea fisierelor bonuri cu numele clientului in folderul in care sunt si listele lor de cumparaturi
    os.chdir(sys.argv[2])
    lista = os.listdir(os.chdir(sys.argv[2]))
    nume_client = i.lstrip("lista_cumparaturi_")
    nume_client = nume_client.strip(".tx")
    with open(f"bon_fiscal_{nume_client}.txt", mode="a") as f:
        f.write(cos.elibereaza_bon())

    for key, value in client.lista_de_produse.items():
        if key in produse.nume:
            ind=produse.nume.index(key)
        else:
            print(f"Produsul {key} nu exista in magazin.")
            continue

        if produse.stoc[ind] == 0:
            print(f"Produsul {key} nu poate fi cumparat.")
            continue

        produse.stoc[ind] = produse.stoc[ind] - value#principiu:daca cantitatea dorita de client depaseste stocul
                                                     #scadem din stoc cantitatea, stocul<0
                                                     #adaugam 1 in stoc pana cand acesta =0, in timp ce din cantitatea dorita scadem 1
                                                     #si obtinem cantitatea care poate fi cumparata
        if produse.stoc[ind] < 0:
            print("Nu mai avem cantitatea dorita in stoc.")
            while produse.stoc[ind] < 0:
                client.lista_de_produse[key] = client.lista_de_produse[key] - 1
                produse.stoc[ind] = produse.stoc[ind] + 1
                value=produse.stoc[ind]
            #print(f"Avem ramase {client.lista_de_produse[key]} bucati de {key} pe care vi le putem da, in urma acestei actiuni stocul devine {produse.stoc[ind]} pentru {key}.")  # am bluca infinita aici

        cos.lista_de_produse.append([key,value])
        cos.adauga_produs(key, client.lista_de_produse[key])
        print(cos.lista_de_produse)

        #prin client.buget-total se modifica valoarea care poate fi achitata din bugetul initial
        #error-free pentru cazul in care bugetul este mai mic decat suma totala care ar fi putut fi achitata pentru avand in vedere cantitatea ceruta
        if total!=0:
            subtotal=client.plateste(client.buget-total)
        else:
            subtotal = client.plateste(client.buget)
        print(f"plata subtotal {subtotal}")

        with open(f"bon_fiscal_{nume_client}.txt", mode="a") as f:
            f.write(cos.adauga_produs(key, client.lista_de_produse[key]))
            f.write(f"....{subtotal} lei")
            f.write("\n")

        #pretul final
        total=total+subtotal
    with open(f"bon_fiscal_{nume_client}.txt", mode="a") as f:
        f.write(f"Totalul este de {total} lei.")
