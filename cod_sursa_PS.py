from collections import deque
import numpy as np
import matplotlib.pyplot as plt
def simulare_joc_razboi():
    pachet = list(range(2, 15)) * 4
    np.random.shuffle(pachet)

    jucator1 = deque(pachet[:26])
    jucator2 = deque(pachet[26:])

    runde = 0
    razboaie = 0
    while jucator1 and jucator2:
        runde += 1
        carte1 = jucator1.popleft()
        carte2 = jucator2.popleft()

        if carte1 > carte2:
            jucator1.extend([carte1, carte2])
        elif carte2 > carte1:
            jucator2.extend([carte2, carte1])
        else:
            # Război
            carti_in_joc = [carte1, carte2]
            razboaie += 1
            numar_carti_razboi = carte1
            while True:
                nr_carti1 = len(jucator1)
                nr_carti2 = len(jucator2)
                if nr_carti1 + nr_carti2 == 0:
                    break
                for _ in range(numar_carti_razboi):
                    if nr_carti1 + nr_carti2 == 0:
                        break
                    runde += 1
                    if nr_carti1 > 0:
                        carte1 = jucator1.popleft()
                        carti_in_joc.append(carte1)
                        nr_carti1 -= 1
                    if nr_carti2 > 0:
                        carte2 = jucator2.popleft()
                        carti_in_joc.append(carte2)
                        nr_carti2 -= 1
                if carte1 > carte2:
                    jucator1.extend(carti_in_joc)
                    break
                elif carte2 > carte1:
                    jucator2.extend(carti_in_joc)
                    break
                else:
                    razboaie += 1
                    numar_carti_razboi = carte1
    return(runde, razboaie)
def histo(valori):
    plt.hist(valori, bins=50, ec='black', density='true', color='lime')
    plt.show()
def histo_redusa(valori):
    valori_reduse = []
    for x in valori:
        if x <= 200:
            valori_reduse.append(x)
    plt.hist(valori_reduse, bins= 50, ec='black', density='true', color='lime')
    plt.show()
def runde_razboaie(runde, razboaie):
    plt.scatter(runde, razboaie, color='blue', alpha=0.1)
    plt.show()
def simulari(n):
    runde = np.array([])
    for i in range(n):
        nr_runde, nr_razboaie = simulare_joc_razboi()
        runde = np.append(runde, nr_runde)
    return np.mean(runde)
def verificare_tlc(miu, sigma):
    lista_deviatii = []
    for i in range(20, 501):
        Sn = simulari(i)
        lista_deviatii.append((np.sqrt(i) / sigma) * (Sn - miu))
    histo(lista_deviatii)
def chernoff_hoeffding(probabilitate, epsilon, prag_superior):
    return np.log(probabilitate / 2) * np.pow((prag_superior - 26), 2) / ((-2) * (epsilon ** 2))
def chernoff_hoeffding_grafic():
    spatiu = np.linspace(1/100, 1, 100)
    plt.plot(spatiu, chernoff_hoeffding(spatiu, 1, 400), color='red')
    plt.show()
def aproximare(n):
    return simulari(n) - 120
def evolutie_aproximari():
    spatiu = np.array([i for i in range(20,1000)])
    diferente = []
    for i in spatiu:
        diferente.append(aproximare(i))
    plt.plot(spatiu, diferente, color = 'orange')
    plt.show()
nr_simulari = 100000
runde = np.array([])
razboaie = []
razboaie_peste360 = []
for i in range(nr_simulari):
    nr_runde, nr_razboaie = simulare_joc_razboi()
    runde = np.append(runde, nr_runde)
    razboaie.append(nr_razboaie)
    if nr_runde >= 360:
        razboaie_peste360.append(nr_razboaie)
med_runde = np.mean(runde)
med_razboaie = np.mean(razboaie)
proc_runde_peste360 = np.sum(runde >= 360) / nr_simulari * 100
print(f"Am avut o medie de {med_runde} runde cu deviatia standard de {np.std(runde)}")
print(f"{proc_runde_peste360} % din runde au durat peste o ora")
print(f"Cea mai scurta runda a durat {np.min(runde)} runde iar cea mai lunga {np.max(runde)} runde")
print(f"O runda obisnuita are, in medie, {med_razboaie} razboaie. Una mai lunga de o ora are {np.mean(razboaie_peste360)}")
#histo(runde)
#histo_redusa(runde)
#runde_reduse = []
#razboaie_reduse = []
#for i in range(len(runde)):
#    if runde[i] < 200:
#        runde_reduse.append(runde[i])
#       razboaie_reduse.append(razboaie[i])
#runde_razboaie(runde_reduse, razboaie_reduse)
#verificare_tlc(120, 82)
#evolutie_aproximari()