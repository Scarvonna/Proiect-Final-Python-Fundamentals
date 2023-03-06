#PARAMETRII IN EDIT CONFIGURATION SUNT TRECUTI CA ABSOLUTE PATH
#trebuie adaugati inaintea rularii fisierului deoarece parametrii nu se salveaza
import os
import sys
import Produs
import Client
import CosDeCumparaturi

f = open(sys.argv[1], mode='r')
a = f.readlines()
f.close()
nr = 0
produse = Produs.Produs([], [], [])
for i in a:
    b, c, d = a[nr].partition(",")
    e, f, g = d.partition(",")  # complica m as mai rau
    produse.nume.append(b), produse.stoc.append(int(e)), produse.pret.append(int(g.strip("\n")))#modificat prin int
    nr += 1
print(produse.nume, produse.stoc, produse.pret)

os.chdir(sys.argv[2])
lista=os.listdir(os.chdir(sys.argv[2]))

numarul = 0


for i in lista:  # se face pentru fiecare client in parte asta
    j = open(lista[numarul], mode="r")
    k = j.readlines()# k este lista de cumparaturi a fiecarui client
    j.close()

    #creare instante Client
    valoare = Client.Client([], [])
    valoare.lista_de_produse={}

    #creare instante CosDeCumparaturi
    cos= CosDeCumparaturi.CosDeCumparaturi({})

    TOTAL=""
    sum=0#folosite pentru generarea bonului fiscal

    numarul += 1
    pozitie = 1

    for x in k:# x reprezinta liniile din lista
        if pozitie>=len(k):
            break
        valoare.buget = k[0]
        a, b, c = k[pozitie].partition(',')
        pozitie = pozitie+1

        c = int(c)
        valoare.lista_de_produse.update({a:c})#DICTIONAR

    print(valoare.buget, valoare.lista_de_produse)
    de_achitat=0
    for i in valoare.lista_de_produse:
        if i in produse.nume:
            ind=produse.nume.index(i)#pentru iterare prin pozitiile listei

            if produse.stoc[ind] == 0:
                    print(f"Produsul {i} nu poate fi cumparat.")
                    continue
            produse.stoc[ind] = produse.stoc[ind] - valoare.lista_de_produse[i]
            if produse.stoc[ind] < 0:
                print("Nu mai avem cantitatea dorita in stoc.")
                while produse.stoc[ind]<0:
                    valoare.lista_de_produse[i]=valoare.lista_de_produse[i]-1
                    produse.stoc[ind] = produse.stoc[ind] + 1
                print(f"Avem ramase {valoare.lista_de_produse[i]} bucati de {i} pe care vi le putem da, in urma acestei actiuni stocul devine {produse.stoc[ind]} pentru {i}.")#am bluca infinita aici

            cos.lista_de_produse.update({f"{i}": [valoare.lista_de_produse[i], produse.pret[ind]]})#cantitate, pret

            if cos.lista_de_produse=={}:
                continue#nu se face metoda de adauga_produs in cazul in care nimic nu poate fi cumparat
            cos.adauga_produs(f"{i}",f"{valoare.lista_de_produse[i]}xbuc",f"{produse.pret[ind]*valoare.lista_de_produse[i]} lei")

            de_achitat=de_achitat+valoare.lista_de_produse[i]*produse.pret[ind]

            os.chdir(sys.argv[2])
            with open(f"bon_fiscal{numarul}.txt", mode="a") as f:
                f.write(f"{i}, {valoare.lista_de_produse[i]}xbuc, {produse.pret[ind] * valoare.lista_de_produse[i]} lei\n")

            sum=sum+produse.pret[ind] * valoare.lista_de_produse[i]
            TOTAL=f"Pret total {sum} lei"

        else:
            print(f"Produsul {i} nu va exista in magazin nici dupa aprovizionare.")

    if sum==0:
        continue#nu se genereaza fisier daca nu poate fi nimic cumparat
    with open(f"bon_fiscal{numarul}.txt", mode="a") as f:
        f.write(TOTAL)

    print(cos.lista_de_produse)

    print(valoare.plateste(de_achitat))