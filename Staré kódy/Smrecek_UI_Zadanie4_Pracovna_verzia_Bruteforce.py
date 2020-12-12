import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
from datetime import datetime
import kdtree
import math


def zaciatok_funkcie(funkcia, zac):
    """Pomocna debuggovacia funkcia ktora vypise ktora funkcia bola prave spustena a ukoncena.

    :param funkcia: nazov funkcie
    :param zac: boolean ci zacina alebo konci
    :return:
    """

    if zac:
        text = "# Zaciatok funkcie {} #".format(funkcia)
    else:
        text = "# Koniec funkcie {} #".format(funkcia)

    ram = "#" * (len(text))

    print(ram)
    print(text)
    print(ram)


def oddelovac(znak="-", pocet=150):
    """Funkcia na vizualnne oddelenie vystupov v konzole

    :param znak: znak oddelovaca
    :param pocet: kolkokrat sa ma oddelovac vypisat
    :return:
    """
    print(znak * pocet)


def casova_pecat(pripona, charakteristika=""):
    """Funkcia na vytvorenie nazvu suboru s casom jeho vzniku

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


# --------------------------------------------------------------------------------------------------------------------
ROZMER_MATICE = 1001
POLOVICA_ROZMERU = ROZMER_MATICE // 2
HORNA_HRANICA = POLOVICA_ROZMERU
DOLNA_HRANICA = -POLOVICA_ROZMERU
OHRANICENIE = POLOVICA_ROZMERU // 10
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
MAX_POCET_BODOV_TRIEDY = (ROZMER_MATICE - 1) // 2
NESPRAVNE_VYGENEROVANE = 0

SPRAVNE_OKLASIFIKOVANE = 0
NESPRAVNE_OKLASIFIKOVANE = 0


def vypis(matica):
    for i in matica:
        print(i)
    oddelovac()


def vizualizuj(matica, charakteristika, uloz = False):
    colors = ["white", "red", "green", "blue", "purple"]
    bounds = [BIELA, CERVENA, ZELENA, MODRA, FIALOVA, 5]
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    extent = [DOLNA_HRANICA, HORNA_HRANICA, DOLNA_HRANICA, HORNA_HRANICA]
    # plt.figure(figsize=(20, 20))
    plt.imshow(matica, interpolation="none", cmap=cmap, norm=norm, extent=extent, origin="lower")

    nazov = casova_pecat(".png", charakteristika)
    plt.title(charakteristika)
    plt.text(DOLNA_HRANICA, DOLNA_HRANICA-(0.12 * ROZMER_MATICE), nazov)

    if uloz:
        plt.savefig(nazov)
    else:
        plt.show()


def vytvor_maticu(pole_vlozenych):
    matica = [[0 for i in range(ROZMER_MATICE)] for j in range(ROZMER_MATICE)]

    for bod in pole_vlozenych:
        vloz_do_matice(matica, bod[0], bod[1], bod[2])

    return matica


def vloz_do_matice(matica, x, y, farba):
    xx, yy = prerataj_suradnice(x, y)
    try:
        matica[yy][xx] = farba
    except IndexError:
        print(x, y, xx, yy)


def ziskaj_farbu_z_matice(matica, x, y):
    if x is None or y is None:
        return -5
    xx, yy = prerataj_suradnice(x, y)

    try:
        return matica[yy][xx]
    except IndexError:
        print(x, y, xx, yy)


def prenasob_suradnice():
    pomocne_cervene = []
    pomocne_zelene = []
    pomocne_modre = []
    pomocne_fialove = []

    for i in range(5):
        pomocne_cervene.append([ZADANE_CERVENE[i][0] // KOEFICIENT, ZADANE_CERVENE[i][1] // KOEFICIENT])
        pomocne_zelene.append([ZADANE_ZELENE[i][0] // KOEFICIENT, ZADANE_ZELENE[i][1] // KOEFICIENT])
        pomocne_modre.append([ZADANE_MODRE[i][0] // KOEFICIENT, ZADANE_MODRE[i][1] // KOEFICIENT])
        pomocne_fialove.append([ZADANE_FIALOVE[i][0] // KOEFICIENT, ZADANE_FIALOVE[i][1] // KOEFICIENT])

    # print(pomocne_cervene)
    # print(pomocne_zelene)
    # print(pomocne_modre)
    # print(pomocne_fialove)

    return pomocne_cervene, pomocne_zelene, pomocne_modre, pomocne_fialove


def prerataj_suradnice(x, y):
    x_matica = x + POLOVICA_ROZMERU
    y_matica = y + POLOVICA_ROZMERU

    return x_matica, y_matica


def vloz_povodnych_20():
    cervene, zelene, modre, fialove = prenasob_suradnice()

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


def vykresli_hranice(matica):
    # print(OHRANICENIE)

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
    r, g, b, p, w = 0, 0, 0, 0, 0

    for i in range(ROZMER_MATICE):
        for j in range(ROZMER_MATICE):
            if matica[i][j] == CERVENA:
                r += 1
            elif matica[i][j] == MODRA:
                b += 1
            elif matica[i][j] == ZELENA:
                g += 1
            elif matica[i][j] == FIALOVA:
                p += 1
            elif matica[i][j] == BIELA:
                w += 1

    print("R", r)
    print("G", g)
    print("B", b)
    print("P", p)
    print("W", w)
    oddelovac()


def vypis_rozmedzie():
    print("R x:", R_x_graf)
    print("R y:", R_y_graf)

    print("G x:", G_x_graf)
    print("G y:", G_y_graf)

    print("B x:", B_x_graf)
    print("B y:", B_y_graf)

    print("P x:", P_x_graf)
    print("P y:", P_y_graf)

    for i in R_x_graf:
        print(i, end=" ")
    print()
    for i in G_x_graf:
        print(i, end=" ")
    print()


def pravdepodobnost():

    cislo = np.random.rand()

    if cislo >= 0.99:
        return False
    else:
        return True


def generuj_farbu_nahodne():
    global POSLEDNA
    global POCETNOST

    farba = np.random.randint(1, 5)
    while farba == POSLEDNA or POCETNOST[farba] >= MAX_POCET_BODOV_TRIEDY:
        farba = np.random.randint(1, 5)

    POSLEDNA = farba
    POCETNOST[farba] += 1

    return farba


def generuj_farbu_v_poradi():
    global POSLEDNA
    global POCETNOST

    farba = BIELA

    if POSLEDNA == BIELA and POCETNOST[CERVENA] < MAX_POCET_BODOV_TRIEDY:
        farba = CERVENA
    if POSLEDNA == CERVENA and POCETNOST[ZELENA] < MAX_POCET_BODOV_TRIEDY:
        farba = ZELENA
    if POSLEDNA == ZELENA and POCETNOST[MODRA] < MAX_POCET_BODOV_TRIEDY:
        farba = MODRA
    if POSLEDNA == MODRA and POCETNOST[FIALOVA] < MAX_POCET_BODOV_TRIEDY:
        farba = FIALOVA
    if POSLEDNA == FIALOVA and POCETNOST[CERVENA] < MAX_POCET_BODOV_TRIEDY:
        farba = CERVENA

    if farba == BIELA:
        print("CHYBA PROGRAMU")

    POSLEDNA = farba
    POCETNOST[farba] += 1

    return farba


def generuj_nespravne_suradnice(rangeX, rangeY):
    x = np.random.randint(DOLNA_HRANICA, HORNA_HRANICA + 1)
    y = np.random.randint(DOLNA_HRANICA, HORNA_HRANICA + 1)
    while x in rangeX or y in rangeY:
        x = np.random.randint(DOLNA_HRANICA, HORNA_HRANICA + 1)
        y = np.random.randint(DOLNA_HRANICA, HORNA_HRANICA + 1)

    return x, y


def generuj_cervene():
    vygenerovane_pole_cervenych = []

    global NESPRAVNE_VYGENEROVANE

    while len(vygenerovane_pole_cervenych) < MAX_POCET_BODOV_TRIEDY:
        spravne = pravdepodobnost()

        if spravne:
            x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            while [x, y] in vygenerovane_pole_cervenych:
                x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
                y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
        else:
            NESPRAVNE_VYGENEROVANE += 1
            x, y = generuj_nespravne_suradnice(R_x_graf, R_y_graf)
            while [x, y] in vygenerovane_pole_cervenych:
                x, y = generuj_nespravne_suradnice(R_x_graf, R_y_graf)

        vygenerovane_pole_cervenych.append([x, y, CERVENA])

    return vygenerovane_pole_cervenych


def generuj_zelene():
    vygenerovane_pole_zelenych = []

    global NESPRAVNE_VYGENEROVANE

    while len(vygenerovane_pole_zelenych) < MAX_POCET_BODOV_TRIEDY:
        spravne = pravdepodobnost()

        if spravne:
            x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            while [x, y] in vygenerovane_pole_zelenych:
                x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
                y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
        else:
            NESPRAVNE_VYGENEROVANE += 1
            x, y = generuj_nespravne_suradnice(G_x_graf, G_x_graf)
            while [x, y] in vygenerovane_pole_zelenych:
                x, y = generuj_nespravne_suradnice(G_x_graf, G_x_graf)

        vygenerovane_pole_zelenych.append([x, y, ZELENA])

    return vygenerovane_pole_zelenych


def generuj_modre():
    vygenerovane_pole_modrych = []

    global NESPRAVNE_VYGENEROVANE

    while len(vygenerovane_pole_modrych) < MAX_POCET_BODOV_TRIEDY:
        spravne = pravdepodobnost()

        if spravne:
            x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            while [x, y] in vygenerovane_pole_modrych:
                x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
                y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
        else:
            NESPRAVNE_VYGENEROVANE += 1
            x, y = generuj_nespravne_suradnice(B_x_graf, B_x_graf)
            while [x, y] in vygenerovane_pole_modrych:
                x, y = generuj_nespravne_suradnice(B_x_graf, B_x_graf)

        vygenerovane_pole_modrych.append([x, y, MODRA])

    return vygenerovane_pole_modrych


def generuj_fialove():
    vygenerovane_pole_fialovych = []

    global NESPRAVNE_VYGENEROVANE

    while len(vygenerovane_pole_fialovych) < MAX_POCET_BODOV_TRIEDY:
        spravne = pravdepodobnost()

        if spravne:
            x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            while [x, y] in vygenerovane_pole_fialovych:
                x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
                y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
        else:
            NESPRAVNE_VYGENEROVANE += 1
            x, y = generuj_nespravne_suradnice(P_x_graf, P_x_graf)
            while [x, y] in vygenerovane_pole_fialovych:
                x, y = generuj_nespravne_suradnice(P_x_graf, P_x_graf)

        vygenerovane_pole_fialovych.append([x, y, FIALOVA])

    return vygenerovane_pole_fialovych


def generuj_pole_suradnic():

    cervene = generuj_cervene()
    zelene = generuj_zelene()
    modre = generuj_modre()
    fialove = generuj_fialove()

    pole_suradnic = []

    for i in range(MAX_POCET_BODOV_TRIEDY):
        pole_suradnic.append(cervene[i])
        pole_suradnic.append(zelene[i])
        pole_suradnic.append(modre[i])
        pole_suradnic.append(fialove[i])

    return pole_suradnic


def kontrola_generatora(pole_suradnic):
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


def klasifikator(pole_vlozenych, x, y, k):
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
    xa = suradnice_a[0]
    ya = suradnice_a[1]
    xb = suradnice_b[0]
    yb = suradnice_b[1]

    vzdialenost = math.sqrt(((xa-xb)**2 + (ya-yb)**2))
    return vzdialenost


def vytvor_testovaciu_sadu(pole_vlozenych, pole_na_vkladanie, k):

    start = time.time()
    for i in  range(MAX_POCET_BODOV_TRIEDY*4):
        if i % 1000 == 0:
            print("Vlozenie {} b zabralo celkovo {} s".format(i, time.time()-start))

        bod = pole_na_vkladanie.pop()

        farba_z_klasifikatora = klasifikator(pole_vlozenych, bod[0], bod[1], k)

        pole_vlozenych.append([bod[0], bod[1], farba_z_klasifikatora])

        global SPRAVNE_OKLASIFIKOVANE
        global NESPRAVNE_OKLASIFIKOVANE

        if farba_z_klasifikatora == bod[2]:
            SPRAVNE_OKLASIFIKOVANE += 1
        else:
            NESPRAVNE_OKLASIFIKOVANE += 1


def zasad_strom(pole_vlozenych):
    bezfarebne = [[x[0], x[1]] for x in pole_vlozenych]

    # print(bezfarebne)

    strom = kdtree.make_kd_tree(bezfarebne, 2)

    return strom


def vyfarbi_mapu(matica, k, strom, skok):
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
    """Hlavna funkcia programu
    
    :return: 
    """
    program_star = time.time()

    np.random.seed(1452)
    k = 1
    pocet_testovacich_bodov = MAX_POCET_BODOV_TRIEDY * 4
    skok = 25
    charakteristika = str(ROZMER_MATICE)+"x-"+str(pocet_testovacich_bodov+20)+"b-"+str(skok)+"p-"+str(k)+"k"


    vlozenie_povodnych_start = time.time()
    pole_vlozenych = vloz_povodnych_20()
    vlozenie_povodnych_end = time.time()
    print("Vlozenie povodnych 20 bodov do pola zabralo {} s".format(vlozenie_povodnych_end - vlozenie_povodnych_start))
    oddelovac()

    generovanie_bodov_start = time.time()
    pole_suradnic = generuj_pole_suradnic()
    # print(pole_suradnic)
    # print(kontrola_generatora(pole_suradnic))
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

    generovanie_matice_start = time.time()
    matica = vytvor_maticu(pole_vlozenych)
    generovanie_matice_end = time.time()
    print("Generovanie matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                  generovanie_matice_end - generovanie_matice_start))
    oddelovac()

    zasadenie_stromu_start = time.time()
    strom = zasad_strom(pole_vlozenych)
    zasadenie_stromu_end = time.time()
    print("Zasadenie stromu zabralo {} s".format(zasadenie_stromu_end - zasadenie_stromu_start))
    oddelovac()

    # with open('C:\\Users\\PeterSmrecek\\Desktop\\Z4 súbory\\10001b_k1_bruteforce_testovacia_sada.npy', 'wb') as f:
    #     np.save(f, matica)

    vyfarbenie_mapy_star = time.time()
    nova_matica = vyfarbi_mapu(matica, k, strom, skok)
    vyfarbenie_mapy_end = time.time()
    print("Vytvorenie novej matice, kde sa nachadza kazdy {}. bod trvalo {}".format(
        skok, vyfarbenie_mapy_end - vyfarbenie_mapy_star))
    oddelovac()

    vizualizacia_start = time.time()
    vizualizuj(nova_matica, charakteristika+"-"+str(uspesnost), uloz=False)
    vizualizacia_end = time.time()
    print("Vizualizacia matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                   vizualizacia_end - vizualizacia_start))
    oddelovac()


    # vykreslenie_hranic_start = time.time()
    # vykresli_hranice(matica)
    # vykreslenie_hranic_end = time.time()
    # print("Vykreslenie hranic do matice o velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
    #                                                                           vykreslenie_hranic_end - vykreslenie_hranic_start))

    # zratanie_bodov_start = time.time()
    # zrataj_pocet_bodov(matica)
    # zratanie_bodov_end = time.time()
    # print("Zratanie bodov v matici o velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
    #                                                                      zratanie_bodov_end - zratanie_bodov_start))




    # --------------------------------------------------------------------------------------------------------------------

    # plt.matshow(matica)
    # plt.colorbar()
    # plt.show()

    # x, y = prerataj_suradnice(-10, -0)
    # vloz_do_matice(matica, x, y, CERVENA)
    # for y in range(-50, 51):
    #     for x in range(-50, 51):
    #         xx, yy = prerataj_suradnice(x, y)
    #         farba = CERVENA if y % 2 == 0 else MODRA
    #         vloz_do_matice(matica, x, y, farba)

    # vizualizacia_start = time.time()
    # vizualizuj_zla(matica, ROZMER_MATICE)
    # vizualizacia_end = time.time()
    # print("Vizualizacia matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE, vizualizacia_end-vizualizacia_start))

    program_end = time.time()
    cas = program_end-program_star
    print("Program pre nastavenia \"{}\" zabral celkovo {} s, co je {} min".format(charakteristika, cas, cas / 60))

if __name__ == "__main__":
    main()
