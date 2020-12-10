import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import random
import time
from datetime import datetime
import kdtree
import math
from tempfile import TemporaryFile


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
        nazov += "-"
        nazov += charakteristika

    nazov += pripona

    return nazov


# --------------------------------------------------------------------------------------------------------------------
ROZMER_MATICE = 10001
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

# BIELA = b"\x00"
# CERVENA = b"\x01"
# ZELENA = b"\x02"
# MODRA = b"\x03"
# FIALOVA = b"\x04"


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

POLE_BODOV = []

# def suradnice(x, y, rozmer_matice):
#     polovica = rozmer_matice // 2
#     x_matica = x + polovica
#     y_matica = y + polovica
#
#     return x_matica, y_matica


def vypis(matica):
    for i in matica:
        print(i)
    oddelovac()


# def vizualizuj_zla(matica, rozmer_matice):
#     plt.xlim(DOLNA_HRANICA, HORNA_HRANICA)
#     plt.ylim(DOLNA_HRANICA, HORNA_HRANICA)
#
#     for i in range(rozmer_matice):
#         for j in range(rozmer_matice):
#             trieda = matica[i][j]
#             farba = None
#             if trieda == b"R":
#                 farba = "ro"
#             elif trieda == b"B":
#                 farba = "bo"
#             elif trieda == b"G":
#                 farba = "go"
#             elif trieda == b"P":
#                 farba = "mo"
#             elif trieda == b"W":
#                 farba = "wo"
#             else:
#                 print("Neznama farba", i, j, trieda)
#
#             # plt.plot(i - POLOVICA_ROZMERU, j - POLOVICA_ROZMERU, farba)
#
#     # plt.show()


def vizualizuj(matica, charakteristika):
    colors = ["white", "red", "green", "blue", "purple"]
    bounds = [BIELA, CERVENA, ZELENA, MODRA, FIALOVA, 5]
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    extent = [DOLNA_HRANICA, HORNA_HRANICA, DOLNA_HRANICA, HORNA_HRANICA]
    plt.figure(figsize=(20, 20))
    plt.imshow(matica, interpolation="none", cmap=cmap, norm=norm, extent=extent, origin="lower")

    # plt.show()
    nazov = casova_pecat(".png", str(ROZMER_MATICE)+"-"+charakteristika)
    plt.title(nazov)
    plt.savefig(nazov)


def vytvor_maticu():
    matica = [[0 for i in range(ROZMER_MATICE)] for j in range(ROZMER_MATICE)]

    # for i in R_y:
    #     for j in R_x:
    #         matica[i][j] = CERVENA
    #
    # for i in G_y:
    #     for j in G_x:
    #         matica[i][j] = ZELENA
    #
    # for i in B_y:
    #     for j in B_x:
    #         matica[i][j] = MODRA
    #
    # for i in P_y:
    #     for j in P_x:
    #         matica[i][j] = FIALOVA

    # vypis(matica)
    return matica


def vloz_do_matice(matica, x, y, farba):
    xx, yy = prerataj_suradnice(x, y)
    try:
        matica[yy][xx] = farba
    except IndexError:
        print(x, y, xx, yy)
    # print("Do matice bol vlozeny bod", x, y, farba)


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


def vloz_povodnych_20(matica):
    cervene, zelene, modre, fialove = prenasob_suradnice()

    for suradnice in cervene:
        x, y = suradnice[0], suradnice[1]
        vloz_do_matice(matica, x, y, CERVENA)
    for suradnice in zelene:
        x, y = suradnice[0], suradnice[1]
        vloz_do_matice(matica, x, y, ZELENA)
    for suradnice in modre:
        x, y = suradnice[0], suradnice[1]
        vloz_do_matice(matica, x, y, MODRA)
    for suradnice in fialove:
        x, y = suradnice[0], suradnice[1]
        vloz_do_matice(matica, x, y, FIALOVA)

    global POLE_BODOV
    POLE_BODOV = cervene + zelene + modre + fialove


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

    # for y in range(-100, 101):
    #     for x in range(-100, 101):
    #         vloz_do_matice(matica, x, y, CERVENA)
    # vypis(matica)


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


def zasad_strom():
    cervene, zelene, modre, fialove = prenasob_suradnice()

    suradnice = cervene + zelene + modre + fialove

    print(suradnice)

    # strom = KDTree.initialize(suradnice)

    strom = kdtree.make_kd_tree(suradnice, 2)

    return strom


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
    # random.seed(1111)
    # cislo = random.random()

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


def generuj_suradnice(matica):
    # farba = generuj_farbu_nahodne()
    farba = generuj_farbu_v_poradi()

    spravny = pravdepodobnost()

    x = None
    y = None

    global NESPRAVNE_VYGENEROVANE
    if not spravny:
        NESPRAVNE_VYGENEROVANE += 1

    if farba == CERVENA and spravny:
        while ziskaj_farbu_z_matice(matica, x, y) != BIELA:
            x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
    elif farba == CERVENA:
        while ziskaj_farbu_z_matice(matica, x, y) != BIELA:
            x, y = generuj_nespravne_suradnice(R_x_graf, R_y_graf)

    if farba == ZELENA and spravny:
        while ziskaj_farbu_z_matice(matica, x, y) != BIELA:
            x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            y = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
    elif farba == ZELENA:
        while ziskaj_farbu_z_matice(matica, x, y) != BIELA:
            x, y = generuj_nespravne_suradnice(G_x_graf, G_x_graf)

    if farba == MODRA and spravny:
        while ziskaj_farbu_z_matice(matica, x, y) != BIELA:
            x = np.random.randint(DOLNA_HRANICA, OHRANICENIE)
            y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
    elif farba == MODRA:
        while ziskaj_farbu_z_matice(matica, x, y) != BIELA:
            x, y = generuj_nespravne_suradnice(B_x_graf, B_x_graf)

    if farba == FIALOVA and spravny:
        while ziskaj_farbu_z_matice(matica, x, y) != BIELA:
            x = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
            y = np.random.randint(-OHRANICENIE + 1, HORNA_HRANICA + 1)
    elif farba == FIALOVA:
        while ziskaj_farbu_z_matice(matica, x, y) != BIELA:
            x, y = generuj_nespravne_suradnice(P_x_graf, P_x_graf)

    return x, y, farba


def kontrola_generatora(x, y, farba):
    if x in R_x_graf and y in R_y_graf and farba == CERVENA:
        return True

    if x in G_x_graf and y in G_y_graf and farba == ZELENA:
        return True

    if x in B_x_graf and y in B_y_graf and farba == MODRA:
        return True

    if x in P_x_graf and y in P_y_graf and farba == FIALOVA:
        return True

    return False


def vzdialenostna_funkcia(suradnice_a, suradnice_b):
    xa = suradnice_a[0]
    ya = suradnice_a[1]
    xb = suradnice_b[0]
    yb = suradnice_b[1]

    vzdialenost = math.sqrt(((xa-xb)**2 + (ya-yb)**2))
    return vzdialenost


def klasifikator(matica, strom, x, y, k):
    # najblizsi_susedia = strom.nearest_neighbor([x, y], n=k)
    najblizsi_susedia = kdtree.get_knn(strom, [x, y], k, 2, vzdialenostna_funkcia, return_distances=False)
    cervena = 0
    zelena = 0
    modra = 0
    fialova = 0

    for sused in najblizsi_susedia:
        # farba_suseda = ziskaj_farbu_z_matice(matica, sused[0][0], sused[0][1])
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


def vytvor_bod(matica, k):
    x, y, farba_z_generatora = generuj_suradnice(matica)

    # print(x, y)

    farba_z_klasifikatora = BIELA

    global POLE_BODOV
    # strom = KDTree.initialize(POLE_BODOV)
    strom = kdtree.make_kd_tree(POLE_BODOV, 2)

    farba_z_klasifikatora = klasifikator(matica, strom, x, y, k)

    global SPRAVNE_OKLASIFIKOVANE
    global NESPRAVNE_OKLASIFIKOVANE

    if farba_z_klasifikatora == farba_z_generatora:
        SPRAVNE_OKLASIFIKOVANE += 1
    else:
        NESPRAVNE_OKLASIFIKOVANE += 1

    vloz_do_matice(matica, x, y, farba_z_klasifikatora)
    # strom.insert([x, y])
    POLE_BODOV.append([x, y])


def vyfarbi_mapu(matica, k):
    global POLE_BODOV
    # strom = KDTree.initialize(POLE_BODOV)

    strom = kdtree.make_kd_tree(POLE_BODOV, 2)

    for x in range(DOLNA_HRANICA, HORNA_HRANICA + 1):
        print("x =", x)
        for y in range(DOLNA_HRANICA, HORNA_HRANICA + 1):
            farba = ziskaj_farbu_z_matice(matica, x, y)
            if farba == BIELA:
                farba_z_klasifikatora = klasifikator(matica, strom, x, y, k)
                vloz_do_matice(matica, x, y, farba_z_klasifikatora)


def main():
    """Hlavna funkcia programu
    
    :return: 
    """
    zaciatok_funkcie(main.__name__, True)

    np.random.seed(1452)
    k = 1

    # generovanie_matice_start = time.time()
    # matica = vytvor_maticu()
    # generovanie_matice_end = time.time()
    # print("Generovanie matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
    #                                                               generovanie_matice_end - generovanie_matice_start))
    #
    # vlozenie_povodnych_start = time.time()
    # vloz_povodnych_20(matica)
    # vlozenie_povodnych_end = time.time()
    # print("Vlozenie povodnych 20 bodov do matice o velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
    #                                                                                    vlozenie_povodnych_end - vlozenie_povodnych_start))
    #
    # vkladanie_bodov_star = time.time()
    # pocet_vlozenych_bodov = MAX_POCET_BODOV_TRIEDY*4
    # for i in range(pocet_vlozenych_bodov):
    #     vytvor_bod(matica, k)
    #     if i % 100 == 0:
    #         vkladanie_bodov_middle = time.time()
    #         print("Bolo vlozenych {} bodov. Trvalo to {} s".format(i, vkladanie_bodov_middle - vkladanie_bodov_star))
    # vkladanie_bodov_end = time.time()
    # print("Vlozenie {} bodov do matice velkosti {}x{} zabralo {} s".format(pocet_vlozenych_bodov, ROZMER_MATICE,
    #                                                                        ROZMER_MATICE, vkladanie_bodov_end - vkladanie_bodov_star))
    #
    # with open('C:\\Users\\PeterSmrecek\\Desktop\\Z4 súbory\\10001b_k1.npy', 'wb') as f:
    #     np.save(f, matica)


    # with open('C:\\Users\\PeterSmrecek\\Desktop\\Z4 súbory\\10001b_k1.npy', 'rb') as f:
    #     matica = np.load(f)
    # vyfarbenie_mapy_star = time.time()
    # vyfarbi_mapu(matica, k)
    # vyfarbenie_mapy_end = time.time()
    # print("Vyfarbenie matice {}x{} v ktorej je uz {} bodov trvalo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
    #                                                                            len(POLE_BODOV),
    #                                                                            vyfarbenie_mapy_end-vyfarbenie_mapy_star))
    # with open('C:\\Users\\PeterSmrecek\\Desktop\\Z4 súbory\\10001b_k1_vyfarbene.npy', 'wb') as f:
    #     np.save(f, matica)



    # vypis_rozmedzie()
    #
    # false = 0
    # true = 0
    # for i in range(100):
    #     if pravdepodobnost():
    #         true += 1
    #     else:
    #         false += 1
    # print(true, false)

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



    with open('C:\\Users\\PeterSmrecek\\Desktop\\Z4 súbory\\10001b_k1_vyfarbene.npy', 'rb') as f:
        matica = np.load(f)

    vizualizacia_start = time.time()
    vizualizuj(matica, "test-vkladania-github")
    vizualizacia_end = time.time()
    print("Vizualizacia matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                   vizualizacia_end - vizualizacia_start))

    # suradnice = []
    # for i in range(400):
    #     suradnice.append(generuj_suradnice(matica))
    #     # print(i, generuj_suradnice())
    #     # if i > 390:
    #     #     print(POCETNOST)
    # print(suradnice)
    # spravne = 0
    # nespravne = 0
    # for i in suradnice:
    #     if kontrola_generatora(i[0], i[1], i[2]):
    #         spravne += 1
    #     else:
    #         nespravne += 1
    # print(spravne, nespravne)
    # print(NESPRAVNE_VYGENEROVANE)

    # --------------------------------------------------------------------------------------------------------------------

    # zasadenie_stromu_start = time.time()
    # strom = zasad_strom()
    # zasadenie_stromu_end = time.time()
    # print("Zasadenie stromu zabralo {} s".format(zasadenie_stromu_end - zasadenie_stromu_start))

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

    zaciatok_funkcie(main.__name__, False)


if __name__ == "__main__":
    main()
