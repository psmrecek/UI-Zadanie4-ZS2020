import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
from datetime import datetime
import kdtree
import math
import os


# --------------------------------------------------------------------------------------------------------------------
ROZMER_MATICE = 10001
MAX_POCET_BODOV_TRIEDY = 5000
POLOVICA_ROZMERU = 5000
HORNA_HRANICA = POLOVICA_ROZMERU
DOLNA_HRANICA = -POLOVICA_ROZMERU
OHRANICENIE = 500
KOEFICIENT = 10000 // (ROZMER_MATICE - 1)

# --------------------------------------------------------------------------------------------------------------------
R_y_matica = range(0, POLOVICA_ROZMERU + OHRANICENIE)
R_x_matica = range(0, POLOVICA_ROZMERU + OHRANICENIE)

G_y_matica = range(0, POLOVICA_ROZMERU + OHRANICENIE)
G_x_matica = range(POLOVICA_ROZMERU - OHRANICENIE, ROZMER_MATICE)

B_y_matica = range(POLOVICA_ROZMERU - OHRANICENIE, ROZMER_MATICE)
B_x_matica = range(0, POLOVICA_ROZMERU + OHRANICENIE)

P_y_matica = range(POLOVICA_ROZMERU - OHRANICENIE, ROZMER_MATICE)
P_x_matica = range(POLOVICA_ROZMERU - OHRANICENIE, ROZMER_MATICE)

R_y_graf = range(DOLNA_HRANICA, OHRANICENIE)
R_x_graf = range(DOLNA_HRANICA, OHRANICENIE)

G_y_graf = range(DOLNA_HRANICA, OHRANICENIE)
G_x_graf = range(-OHRANICENIE + 1, HORNA_HRANICA + 1)

B_y_graf = range(-OHRANICENIE + 1, HORNA_HRANICA + 1)
B_x_graf = range(DOLNA_HRANICA, OHRANICENIE)

P_y_graf = range(-OHRANICENIE + 1, HORNA_HRANICA + 1)
P_x_graf = range(-OHRANICENIE + 1, HORNA_HRANICA + 1)

# --------------------------------------------------------------------------------------------------------------------
BIELA = 0
CERVENA = 1
ZELENA = 2
MODRA = 3
FIALOVA = 4

# --------------------------------------------------------------------------------------------------------------------
ZADANE_CERVENE = [[-4500, -4400], [-4100, -3000], [-1800, -2400], [-2500, -3400], [-2000, -1400]]
ZADANE_ZELENE = [[4500, -4400], [4100, -3000], [1800, -2400], [2500, -3400], [2000, -1400]]
ZADANE_MODRE = [[-4500, 4400], [-4100, 3000], [-1800, 2400], [-2500, 3400], [-2000, 1400]]
ZADANE_FIALOVE = [[4500, 4400], [4100, 3000], [1800, 2400], [2500, 3400], [2000, 1400]]

POSLEDNA = BIELA
POCETNOST = [0, 0, 0, 0, 0]
NESPRAVNE_VYGENEROVANE = 0

SPRAVNE_OKLASIFIKOVANE = 0
NESPRAVNE_OKLASIFIKOVANE = 0

POLE_NESPRAVNYCH_SURADNIC = []
POLE_SURADNIC = ZADANE_CERVENE + ZADANE_ZELENE + ZADANE_MODRE + ZADANE_FIALOVE


def oddelovac(znak="-", pocet=150):
    """Funkcia na vizualnne oddelenie vystupov v konzole

    :param znak: znak oddelovaca
    :param pocet: kolkokrat sa ma oddelovac vypisat
    :return:
    """
    print(znak * pocet)


def casova_pecat(pripona, charakteristika=""):
    """Funkcia na vytvorenie nazvu suboru s casom jeho  a charakteristikou

    :param pripona: suboru
    :param charakteristika: text nasledujuci za datumom a casom
    :return: nazov suboru
    """
    cas = datetime.now()
    nazov = cas.strftime("%Y-%m-%d--%H-%M-%S")

    if charakteristika != "":
        nazov += "--"
        nazov += charakteristika + "-Smrecek"

    nazov += pripona

    return nazov


def nacitaj_cislo(dolna_hranica, horna_hranica):
    """Pomocna funkcia na nacitanie cisla s osetrenim hranic

    :param dolna_hranica:
    :param horna_hranica:
    :return:
    """
    while True:
        try:
            cislo = int(input("Zadaj cislo z intervalu <{} az {}>: ".format(dolna_hranica, horna_hranica)))
            if dolna_hranica <= cislo <= horna_hranica:
                return cislo
            else:
                print("Zadane cislo nie je z intervalu <{} az {}>".format(dolna_hranica, horna_hranica))
        except:
            print("Nebolo zadane cislo")


def binarna_volba():
    """Pomocna funkcia na zistenie najhlbsich tuzob pouzivatela

    :return: boolean
    """
    while True:
        vstup = input("Zadaj a pre ANO, zadaj n pre NIE: ")
        if vstup == "a":
            return True
        if vstup == "n":
            return False
        print("Nespravny vstup")


def vizualizuj_maticu(matica, charakteristika, uloz=False):
    """Funkcia na vizualizaciu matice

    :param matica: 2D pole
    :param charakteristika: popisovy text obrazka
    :param uloz: True ak ulozit ako obrazok, False ak len zobrazit
    :return:
    """
    colors = ["white", "red", "green", "blue", "purple"]
    bounds = [BIELA, CERVENA, ZELENA, MODRA, FIALOVA, 5]
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    extent = [DOLNA_HRANICA, HORNA_HRANICA, DOLNA_HRANICA, HORNA_HRANICA]
    plt.figure(figsize=(9, 9))
    plt.imshow(matica, interpolation="none", cmap=cmap, norm=norm, extent=extent, origin="lower")

    nazov = casova_pecat(".png", charakteristika)
    plt.title(charakteristika)
    plt.text(DOLNA_HRANICA, DOLNA_HRANICA-(0.12 * ROZMER_MATICE), nazov)

    if uloz:
        plt.savefig(nazov)
    else:
        plt.show()

    plt.close()


def vizualizuj_pole(pole_vlozenych, charakteristika, uloz=False):
    """Funkcia na vizualizaciu pola vlozenych suradnic

    :param pole_vlozenych: pole suradnic ktore su uz vlozene do plochy
    :param charakteristika: popisovy text obrazka
    :param uloz: True ak ulozit ako obrazok, False ak len zobrazit
    :return:
    """
    bezfarebne = []
    farby = []

    for i in pole_vlozenych:
        bezfarebne.append([i[0], i[1]])
        if i[2] == CERVENA:
            farby.append("red")
        elif i[2] == ZELENA:
            farby.append("green")
        elif i[2] == MODRA:
            farby.append("blue")
        elif i[2] == FIALOVA:
            farby.append("purple")

    plt.axis("square")
    plt.figure(figsize=(9, 9))
    plt.xlim(DOLNA_HRANICA, HORNA_HRANICA)
    plt.ylim(DOLNA_HRANICA, HORNA_HRANICA)

    plt.scatter(*zip(*pole_vlozenych), c=farby)

    nazov = casova_pecat(".png", charakteristika)
    plt.title(charakteristika)
    plt.text(DOLNA_HRANICA, DOLNA_HRANICA-(0.12 * ROZMER_MATICE), nazov)

    if uloz:
        plt.savefig(nazov)
    else:
        plt.show()

    plt.close()


def vytvor_maticu(pole_vlozenych):
    """Vytvori 2D plochu, vyfarbi ju na bielo a vlozi 20 povodnych bodov

    :param pole_vlozenych: pole bodov na vlozenie do matice
    :return: 2D pole reprezentujuce plochu grafu
    """
    matica = [[0 for i in range(ROZMER_MATICE)] for j in range(ROZMER_MATICE)]

    for bod in pole_vlozenych:
        vloz_do_matice(matica, bod[0], bod[1], bod[2])

    return matica


def vloz_povodnych_20():
    """Do pola vlozi povodnych 20 suradnic zo zadania

    :return: pole suradnic na vlozenie do matice
    """
    cervene, zelene, modre, fialove = ZADANE_CERVENE, ZADANE_ZELENE, ZADANE_MODRE, ZADANE_FIALOVE

    pole_vlozenych = []

    for suradnice in cervene:
        x, y = suradnice[0], suradnice[1]
        pole_vlozenych.append([x, y, CERVENA])
    for suradnice in zelene:
        x, y = suradnice[0], suradnice[1]
        pole_vlozenych.append([x, y, ZELENA])
    for suradnice in modre:
        x, y = suradnice[0], suradnice[1]
        pole_vlozenych.append([x, y, MODRA])
    for suradnice in fialove:
        x, y = suradnice[0], suradnice[1]
        pole_vlozenych.append([x, y, FIALOVA])

    return pole_vlozenych


def vloz_do_matice(matica, x, y, farba):
    """Vlozi bod do matice na urcene miesto

    :param matica: 2D pole
    :param x: suradnnica x
    :param y: suradnica y
    :param farba: farba bodu
    :return:
    """
    xx, yy = prerataj_suradnice(x, y)
    try:
        matica[yy][xx] = farba
    except IndexError:
        print(x, y, xx, yy)


def ziskaj_farbu_z_matice(matica, x, y):
    """Vrati farbu ktora sa nachadza v ploche na konkretnych suradniciach

    :param matica: 2D pole
    :param x: suradnica x
    :param y: suradnica y
    :return: farba konkretneho bodu
    """
    if x is None or y is None:
        return -5
    xx, yy = prerataj_suradnice(x, y)

    try:
        return matica[yy][xx]
    except IndexError:
        print(x, y, xx, yy)


def prerataj_suradnice(x, y):
    """Zmeni suradnice z realnych suradnic plochy na indexy v matici

    :param x: suradnica x v ploche
    :param y: suradnica y v ploche
    :return: suradnice v matici
    """
    x_matica = x + POLOVICA_ROZMERU
    y_matica = y + POLOVICA_ROZMERU

    return x_matica, y_matica


def vykresli_hranice(matica):
    """Funkcia vykresli hranice ploch tried

    :param matica: 2D pole, prazdna matica
    :return:
    """
    for y in range(DOLNA_HRANICA, OHRANICENIE + 1):
        vloz_do_matice(matica, OHRANICENIE, y, CERVENA)
        vloz_do_matice(matica, y, OHRANICENIE, CERVENA)

        vloz_do_matice(matica, -OHRANICENIE, y, ZELENA)
        vloz_do_matice(matica, y, -OHRANICENIE, MODRA)

    for y in range(-OHRANICENIE, HORNA_HRANICA + 1):
        vloz_do_matice(matica, -OHRANICENIE, y, FIALOVA)
        vloz_do_matice(matica, y, -OHRANICENIE, FIALOVA)

        vloz_do_matice(matica, OHRANICENIE, y, MODRA)
        vloz_do_matice(matica, y, OHRANICENIE, ZELENA)


def zrataj_pocet_bodov(matica):
    """Zrata pocet bodov jednotlivych tried v matici

    :param matica: 2D pole
    :return:
    """
    r, g, b, p, w = 0, 0, 0, 0, 0

    for i in range(ROZMER_MATICE):
        if i % 1000 == 0:
            print("x =", i)
        for j in range(ROZMER_MATICE):
            if matica[i][j] == BIELA:
                w += 1
                continue
            elif matica[i][j] == CERVENA:
                r += 1
                continue
            elif matica[i][j] == MODRA:
                b += 1
                continue
            elif matica[i][j] == ZELENA:
                g += 1
                continue
            elif matica[i][j] == FIALOVA:
                p += 1

    print("R", r)
    print("G", g)
    print("B", b)
    print("P", p)
    print("W", w)


def pravdepodobnost():
    """Generuje pravdepodobnost suradnic bidu nachadzajucich sa v hraniciach svojej triedy

    :return: True ak je bod v hraniciach prisluchajucich svojej triede, False ak ma byt inde
    """
    cislo = np.random.rand()

    if cislo >= 0.99:
        return False
    else:
        return True


def generuj_nespravne_suradnice(rangeX, rangeY):
    """Vygeneruje suradnice mimo bodu triedy mimo plochy tejto triedy

    :param rangeX: rozsah suradnice x triedy
    :param rangeY: rozsah suradnice y triedy
    :return: bpd mimo rozsahu tychto suradnic
    """
    global POLE_NESPRAVNYCH_SURADNIC

    x = np.random.randint(DOLNA_HRANICA, HORNA_HRANICA + 1)
    y = np.random.randint(DOLNA_HRANICA, HORNA_HRANICA + 1)
    while (x in rangeX or y in rangeY) or [x, y] in POLE_NESPRAVNYCH_SURADNIC:
        x = np.random.randint(DOLNA_HRANICA, HORNA_HRANICA + 1)
        y = np.random.randint(DOLNA_HRANICA, HORNA_HRANICA + 1)

    POLE_NESPRAVNYCH_SURADNIC.append([x, y])

    return x, y


def generuj_cervene():
    """Vygeneruje pole jedinecnych cervenych suradnic

    :return: pole cervenych suradnic
    """
    vygenerovane_pole_cervenych = []

    global NESPRAVNE_VYGENEROVANE
    global POLE_SURADNIC

    while len(vygenerovane_pole_cervenych) < MAX_POCET_BODOV_TRIEDY:
        spravne = pravdepodobnost()

        if spravne:
            x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            while [x, y, CERVENA] in vygenerovane_pole_cervenych or [x, y] in POLE_SURADNIC:
                x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
                y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
        else:
            NESPRAVNE_VYGENEROVANE += 1
            x, y = generuj_nespravne_suradnice(R_x_graf, R_y_graf)
            while [x, y, CERVENA] in vygenerovane_pole_cervenych:
                x, y = generuj_nespravne_suradnice(R_x_graf, R_y_graf)

        vygenerovane_pole_cervenych.append([x, y, CERVENA])

    POLE_SURADNIC += [[a[0], a[1]] for a in vygenerovane_pole_cervenych]

    return vygenerovane_pole_cervenych


def generuj_zelene():
    """Vygeneruje pole jedinecnych zelenych suradnic

    :return: pole zelenych suradnic
    """
    vygenerovane_pole_zelenych = []

    global NESPRAVNE_VYGENEROVANE
    global POLE_SURADNIC

    while len(vygenerovane_pole_zelenych) < MAX_POCET_BODOV_TRIEDY:
        spravne = pravdepodobnost()

        if spravne:
            x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            while [x, y, ZELENA] in vygenerovane_pole_zelenych or [x, y] in POLE_SURADNIC:
                x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
                y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
        else:
            NESPRAVNE_VYGENEROVANE += 1
            x, y = generuj_nespravne_suradnice(G_x_graf, G_x_graf)
            while [x, y, ZELENA] in vygenerovane_pole_zelenych:
                x, y = generuj_nespravne_suradnice(G_x_graf, G_x_graf)

        vygenerovane_pole_zelenych.append([x, y, ZELENA])

    POLE_SURADNIC += [[a[0], a[1]] for a in vygenerovane_pole_zelenych]

    return vygenerovane_pole_zelenych


def generuj_modre():
    """Vygeneruje pole jedinecnych modrych suradnic

    :return: pole modrych suradnic
    """
    vygenerovane_pole_modrych = []

    global NESPRAVNE_VYGENEROVANE
    global POLE_SURADNIC

    while len(vygenerovane_pole_modrych) < MAX_POCET_BODOV_TRIEDY:
        spravne = pravdepodobnost()

        if spravne:
            x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            while [x, y, MODRA] in vygenerovane_pole_modrych or [x, y] in POLE_SURADNIC:
                x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
                y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
        else:
            NESPRAVNE_VYGENEROVANE += 1
            x, y = generuj_nespravne_suradnice(B_x_graf, B_x_graf)
            while [x, y, MODRA] in vygenerovane_pole_modrych:
                x, y = generuj_nespravne_suradnice(B_x_graf, B_x_graf)

        vygenerovane_pole_modrych.append([x, y, MODRA])

    POLE_SURADNIC += [[a[0], a[1]] for a in vygenerovane_pole_modrych]

    return vygenerovane_pole_modrych


def generuj_fialove():
    """Vygeneruje pole jedinecnych fialovych suradnic

    :return: pole fialovych suradnic
    """
    vygenerovane_pole_fialovych = []

    global NESPRAVNE_VYGENEROVANE
    global POLE_SURADNIC

    while len(vygenerovane_pole_fialovych) < MAX_POCET_BODOV_TRIEDY:
        spravne = pravdepodobnost()

        if spravne:
            x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            while [x, y, FIALOVA] in vygenerovane_pole_fialovych or [x, y] in POLE_SURADNIC:
                x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
                y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
        else:
            NESPRAVNE_VYGENEROVANE += 1
            x, y = generuj_nespravne_suradnice(P_x_graf, P_x_graf)
            while [x, y, FIALOVA] in vygenerovane_pole_fialovych:
                x, y = generuj_nespravne_suradnice(P_x_graf, P_x_graf)

        vygenerovane_pole_fialovych.append([x, y, FIALOVA])

    POLE_SURADNIC += [[a[0], a[1]] for a in vygenerovane_pole_fialovych]

    return vygenerovane_pole_fialovych


def generuj_pole_suradnic():
    """Zluci prvky poli jednotlivych farieb do jedneho pola kde sa farby striedaju v poradi.

    :return: celkove pole suradnic na vlozenie do plochy
    """
    cervene = generuj_cervene()
    zelene = generuj_zelene()
    modre = generuj_modre()
    fialove = generuj_fialove()

    # print(cervene)
    # oddelovac(znak="c")
    # print(zelene)
    # oddelovac(znak="z")
    # print(modre)
    # oddelovac(znak="m")
    # print(fialove)
    # oddelovac(znak="f")

    pole_suradnic = []

    for i in range(MAX_POCET_BODOV_TRIEDY):
        pole_suradnic.append(cervene[i])
        pole_suradnic.append(zelene[i])
        pole_suradnic.append(modre[i])
        pole_suradnic.append(fialove[i])

    return pole_suradnic


def kontrola_generatora(pole_suradnic):
    """Skontroluje, ci boli vygenerovane spravne suradnice v spravnom poradi v spravnych poctoch

    :param pole_suradnic: pole suradnic na vlozenie do mapy
    :return: pocet suradnic, ktore su vygenerovane v hraniciach svojich tried, pocet suradnic vygenerovanych mimo hranic
                svojich tried
    """
    spravne = 0

    for i in range(0, MAX_POCET_BODOV_TRIEDY*4, 4):
        x, y = pole_suradnic[i][0], pole_suradnic[i][1]
        if x in R_x_graf and y in R_y_graf:
            spravne += 1

        x, y = pole_suradnic[i + 1][0], pole_suradnic[i + 1][1]
        if x in G_x_graf and y in G_y_graf:
            spravne += 1

        x, y = pole_suradnic[i + 2][0], pole_suradnic[i + 2][1]
        if x in B_x_graf and y in B_y_graf:
            spravne += 1

        x, y = pole_suradnic[i + 3][0], pole_suradnic[i + 3][1]
        if x in P_x_graf and y in P_y_graf:
            spravne += 1

    nespravne = MAX_POCET_BODOV_TRIEDY * 4 - spravne

    return spravne, nespravne


def klasifikator_testovacich_bodov(pole_vlozenych, x, y, k):
    """Klasifikator testovacich bodov pomocou kNN
    Pomocou bruteforce metody vypocita vzdialenosti novo vkladaneho bodu od ostatnych vlozenych bodov a na zaklade k
    najblizsich urci farbu, akej bude novy bod.

    :param pole_vlozenych: pole bodov ktore sa uz nachadzaju v ploche
    :param x: suradnica x novo vkladaneho bodu
    :param y: suradnica y novo vkladaneho bodu
    :param k: vstup pre kNN algoritmus
    :return: farba novo vkladaneho bodu
    """
    cervena = 0
    zelena = 0
    modra = 0
    fialova = 0

    farba_z_klasifikatora = BIELA

    pole_vzdialenosti = []

    for vlozeny in pole_vlozenych:
        vzdialenost = vzdialenostna_funkcia([vlozeny[0], vlozeny[1]], [x, y])
        farba_z_klasifikatora = vlozeny[2]
        pole_vzdialenosti.append([vzdialenost, farba_z_klasifikatora])

    pole_vzdialenosti.sort(key=lambda i: i[0])

    for i in range(k):
        farba_suseda = pole_vzdialenosti[i][1]
        if farba_suseda == CERVENA:
            cervena += 1
        elif farba_suseda == ZELENA:
            zelena += 1
        elif farba_suseda == MODRA:
            modra += 1
        elif farba_suseda == FIALOVA:
            fialova += 1
        else:
            print("CHYBA PROGRAMU")

    maximum = np.amax([cervena, zelena, modra, fialova])
    if maximum == cervena:
        farba_z_klasifikatora = CERVENA
    elif maximum == zelena:
        farba_z_klasifikatora = ZELENA
    elif maximum == modra:
        farba_z_klasifikatora = MODRA
    elif maximum == fialova:
        farba_z_klasifikatora = FIALOVA

    return farba_z_klasifikatora


def klasifikator_zvysnych_bodov(matica, strom, x, y, k):
    """Klasifikator bodov pre potreby vyfarbenia mapy
    Pomocou prevzateho KD stromu urci k susedov zadaneho bodu a urci jeho farbu.
    :param matica: 2D pole reprezentujuce plochu
    :param strom: KD strom obsahujuci povodne + testovacie body, ktore su uz v ploche
    :param x: suradnica x bodu na klasifikovanie
    :param y: suradnica y bodu na klasifikovanie
    :param k: vstup pre kNN algoritmus
    :return: farba klasifikovaneho bodu
    """
    najblizsi_susedia = kdtree.get_knn(strom, [x, y], k, 2, vzdialenostna_funkcia, return_distances=False)
    cervena = 0
    zelena = 0
    modra = 0
    fialova = 0

    for sused in najblizsi_susedia:
        farba_suseda = ziskaj_farbu_z_matice(matica, sused[0], sused[1])
        if farba_suseda == CERVENA:
            cervena += 1
        elif farba_suseda == ZELENA:
            zelena += 1
        elif farba_suseda == MODRA:
            modra += 1
        elif farba_suseda == FIALOVA:
            fialova += 1
        else:
            print("CHYBA PROGRAMU")

    maximum = np.amax([cervena, zelena, modra, fialova])
    if maximum == cervena:
        farba_z_klasifikatora = CERVENA
    elif maximum == zelena:
        farba_z_klasifikatora = ZELENA
    elif maximum == modra:
        farba_z_klasifikatora = MODRA
    elif maximum == fialova:
        farba_z_klasifikatora = FIALOVA

    return farba_z_klasifikatora


def vzdialenostna_funkcia(suradnice_a, suradnice_b):
    """Funkcia na vypocet euklidovej vzdialenosti bodov

    :param suradnice_a: pole suradnic bodu a vo formate [x, y]
    :param suradnice_b: pole suradnic bodu b vo formate [x, y]
    :return: vzdialenost 2 bodov
    """
    xa = suradnice_a[0]
    ya = suradnice_a[1]
    xb = suradnice_b[0]
    yb = suradnice_b[1]

    vzdialenost = math.sqrt(((xa-xb)**2 + (ya-yb)**2))
    return vzdialenost


def vytvor_testovaciu_sadu(pole_vlozenych, pole_na_vkladanie, k):
    """Postupne klasifikuje a vklada testovacie body do 2D plochy. Rata pocet spravne a nespravne oklasifikovanych.

    :param pole_vlozenych: pole bodov, ktore su uz v ploche vlozene
    :param pole_na_vkladanie: pole bodov urcenych na vlozenie do plochy
    :param k: vstup pre kNN algoritmus
    :return:
    """
    start = time.time()
    for i in range(MAX_POCET_BODOV_TRIEDY*4):
        if i % 1000 == 0:
            print("Vlozenie {} b zabralo celkovo {} s".format(i, time.time()-start))

        bod = pole_na_vkladanie.pop()

        farba_z_klasifikatora = klasifikator_testovacich_bodov(pole_vlozenych, bod[0], bod[1], k)

        pole_vlozenych.append([bod[0], bod[1], farba_z_klasifikatora])

        global SPRAVNE_OKLASIFIKOVANE
        global NESPRAVNE_OKLASIFIKOVANE

        if farba_z_klasifikatora == bod[2]:
            SPRAVNE_OKLASIFIKOVANE += 1
        else:
            NESPRAVNE_OKLASIFIKOVANE += 1


def zasad_strom(pole_vlozenych):
    """Z pola vlozenych bodov vytvori podla prevzatej implementacie KD strom s vlastnou vzdialenostou funkciou

    :param pole_vlozenych: pole bodov uz vlozenych a oklasifikovanych v 2D ploche
    :return: KD strom
    """
    bezfarebne = [[x[0], x[1]] for x in pole_vlozenych]

    strom = kdtree.make_kd_tree(bezfarebne, 2)

    return strom


def vyfarbi_mapu(matica, k, strom, skok):
    """Funkcia na vyfarbenie zvysnych bodov plochy pre zvyrazneneie hranic ploch urcenych klasifikatorom.

    :param matica: 2D pole reprezentujuce plochu grafu
    :param k: vstup pre kNN algoritmus
    :param strom: KD strom obsahujuci uz vlozene body plochy
    :param skok: cislo reprezentujuce kazdy kolko bod bude klasifikovany
    :return: matica na vizualizaciu
    """
    rozmer_matice = ROZMER_MATICE // skok
    nova_matica = [[0 for x in range(rozmer_matice + 1)] for y in range(rozmer_matice + 1)]
    start = time.time()
    nove_x = 0

    for x in range(DOLNA_HRANICA, HORNA_HRANICA + 1, skok):
        nove_y = 0
        print("x = {}; {} s".format(x, time.time() - start))
        for y in range(DOLNA_HRANICA, HORNA_HRANICA + 1, skok):
            farba = ziskaj_farbu_z_matice(matica, x, y)
            if farba == BIELA:
                farba = klasifikator_zvysnych_bodov(matica, strom, x, y, k)
            nova_matica[nove_y][nove_x] = farba
            nove_y += 1
        nove_x += 1

    return nova_matica


def main():
    """Hlavna funkcia programu. Obsahuje riadic.
    
    :return: 
    """
    np.random.seed(1452)

    vyber = "x"
    charakteristika = ""

    while vyber != "a" and vyber != "b" and vyber != "c":
        print("Zadaj a pre spustenie testovania, "
              "zadaj b pre vykreslenie hranic do mapy a ulozenie matice do suboru, "
              "zadaj c pre vizualizaciu matice zo suboru")

        vyber = input()

    if vyber == "a":
        global MAX_POCET_BODOV_TRIEDY

        print("Zadaj k pre kNN ", end="")
        k = nacitaj_cislo(1, 15)

        print("Zadaj pocet bodov triedy ", end="")
        MAX_POCET_BODOV_TRIEDY = nacitaj_cislo(50, 5000)
        pocet_testovacich_bodov = MAX_POCET_BODOV_TRIEDY * 4

        print("Zadaj kazdy kolky bod si prajes vizualizovat pri vyfarbovani mapy ", end="")
        skok = nacitaj_cislo(1, 100)

        print("Ulozit maticu s vlozenymi testovacimi bodmi do suboru? ", end="")
        uloz_maticu_do_suboru = binarna_volba()
        if uloz_maticu_do_suboru:
            priecinok = input("Zadaj cestu k priecinku, kde ma byt subor s maticou ulozeny: ")

        charakteristika = str(ROZMER_MATICE)+"x-"+str(pocet_testovacich_bodov+20)+"b-"+str(skok)+"p-"+str(k)+"k"

    if vyber == "b":
        priecinok = input("Zadaj cestu k priecinku, kde ma byt subor s maticou ulozeny: ")
        charakteristika = "vykreslenie matice hranic"

    if vyber == "c":
        cesta = input("Zadaj cestu k suboru s maticou: ")

        with open(cesta, 'rb') as f:
            matica = np.load(f)

    program_star = time.time()

    if vyber == "a":
        vlozenie_povodnych_start = time.time()
        pole_vlozenych = vloz_povodnych_20()
        vlozenie_povodnych_end = time.time()
        print("Vlozenie povodnych 20 bodov do pola zabralo {} s".format(vlozenie_povodnych_end - vlozenie_povodnych_start))
        oddelovac()

        generovanie_bodov_start = time.time()
        pole_suradnic = generuj_pole_suradnic()
        print("Pocet suradnic vygnenerovanych mimo svojho ohranicenia", NESPRAVNE_VYGENEROVANE)
        generovanie_bodov_end = time.time()
        print("Vygenerovanie a usporiadanie {} bodov trvalo {} s".format(pocet_testovacich_bodov,
                                                                         generovanie_bodov_end-generovanie_bodov_start))
        oddelovac()

        vkladanie_bodov_star = time.time()
        vytvor_testovaciu_sadu(pole_vlozenych, pole_suradnic, k)
        vkladanie_bodov_end = time.time()
        print("Vlozenie {} bodov do pola zabralo {} s".format(pocet_testovacich_bodov,
                                                              vkladanie_bodov_end - vkladanie_bodov_star))
        oddelovac()

        uspesnost = SPRAVNE_OKLASIFIKOVANE / pocet_testovacich_bodov * 100
        print("Z {} bodov bolo spravne klasifikovanych {} a nespravne {}, co znaci "
              "uspesnost {}%".format(pocet_testovacich_bodov, SPRAVNE_OKLASIFIKOVANE, NESPRAVNE_OKLASIFIKOVANE, uspesnost))
        oddelovac()

        vizualizacia_pola_start = time.time()
        vizualizuj_pole(pole_vlozenych, charakteristika, uloz=True)
        vizualizacia_pola_end = time.time()
        print("Vizualizacia pola vlozenych suradnic o velkosti {} zabrala {} s".format(len(pole_vlozenych),
                                                                       vizualizacia_pola_end - vizualizacia_pola_start))

        generovanie_matice_start = time.time()
        matica = vytvor_maticu(pole_vlozenych)
        generovanie_matice_end = time.time()
        print("Generovanie matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                      generovanie_matice_end - generovanie_matice_start))
        oddelovac()

        if uloz_maticu_do_suboru:
            nazov = charakteristika + ".npy"
            cesta = os.path.join(priecinok, nazov)
            try:
                with open(cesta, 'wb') as f:
                    np.save(f, matica)
            except:
                print("Maticu sa nepodarilo ulozit do suboru.")

        # zratanie_bodov_start = time.time()
        # zrataj_pocet_bodov(matica)
        # zratanie_bodov_end = time.time()
        # print("Zratanie bodov v matici o velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
        #                                                                      zratanie_bodov_end - zratanie_bodov_start))
        # oddelovac()

        zasadenie_stromu_start = time.time()
        strom = zasad_strom(pole_vlozenych)
        zasadenie_stromu_end = time.time()
        print("Zasadenie stromu zabralo {} s".format(zasadenie_stromu_end - zasadenie_stromu_start))
        oddelovac()

        vyfarbenie_mapy_star = time.time()
        nova_matica = vyfarbi_mapu(matica, k, strom, skok)
        vyfarbenie_mapy_end = time.time()
        print("Vytvorenie novej matice, kde sa nachadza kazdy {}. bod trvalo {}".format(
            skok, vyfarbenie_mapy_end - vyfarbenie_mapy_star))
        oddelovac()

        vizualizacia_start = time.time()
        vizualizuj_maticu(nova_matica, charakteristika + "-" + str(uspesnost), uloz=True)
        vizualizacia_end = time.time()
        print("Vizualizacia matice velkosti {}x{} zabrala {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                       vizualizacia_end - vizualizacia_start))
        oddelovac()

    if vyber == "b":
        vykreslenie_hranic_start = time.time()
        matica_hranic = [[0 for x in range(ROZMER_MATICE)] for y in range(ROZMER_MATICE)]
        vykresli_hranice(matica_hranic)
        vykreslenie_hranic_end = time.time()
        print("Vykreslenie hranic do matice o velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                                  vykreslenie_hranic_end - vykreslenie_hranic_start))
        cesta = os.path.join(priecinok, "Matica-hranic.npy")
        with open(cesta, 'wb') as f:
            np.save(f, matica_hranic)

    if vyber == "c":
        nazov_suboru = os.path.basename(cesta)
        charakteristika = nazov_suboru[:-4]
        vizualizacia_start = time.time()
        vizualizuj_maticu(matica, charakteristika, uloz=True)
        vizualizacia_end = time.time()
        print("Vizualizacia matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                       vizualizacia_end - vizualizacia_start))

    program_end = time.time()
    cas = program_end-program_star

    print("Program pre nastavenia \"{}\" zabral celkovo {} s, co je {} min".format(charakteristika, cas, cas / 60))


if __name__ == "__main__":
    main()
