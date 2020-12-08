import matplotlib.pyplot as plt
import matplotlib as mpl
import time
from datetime import datetime


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

# -------------------------------------------------------------------------------------------
ROZMER_MATICE = 10001
POLOVICA_ROZMERU = ROZMER_MATICE // 2
HORNA_HRANICA = POLOVICA_ROZMERU
DOLNA_HRANICA = -POLOVICA_ROZMERU
OHRANICENIE = POLOVICA_ROZMERU // 10
KOEFICIENT = 10000//(ROZMER_MATICE - 1)

# -------------------------------------------------------------------------------------------
R_y = range(0, POLOVICA_ROZMERU + OHRANICENIE)
R_x = range(0, POLOVICA_ROZMERU + OHRANICENIE)

G_y = range(0, POLOVICA_ROZMERU + OHRANICENIE)
G_x = range(POLOVICA_ROZMERU - OHRANICENIE, ROZMER_MATICE)

B_y = range(POLOVICA_ROZMERU - OHRANICENIE, ROZMER_MATICE)
B_x = range(0, POLOVICA_ROZMERU + OHRANICENIE)

P_y = range(POLOVICA_ROZMERU - OHRANICENIE, ROZMER_MATICE)
P_x = range(POLOVICA_ROZMERU - OHRANICENIE, ROZMER_MATICE)


# -------------------------------------------------------------------------------------------
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


# -------------------------------------------------------------------------------------------
ZADANE_CERVENE = [[-4500, -4400], [-4100, -3000], [-1800, -2400], [-2500, -3400], [-2000, -1400]]
ZADANE_ZELENE = [[4500, -4400], [4100, -3000], [1800, -2400], [2500, -3400], [2000, -1400]]
ZADANE_MODRE = [[-4500, 4400], [-4100, 3000], [-1800, 2400], [-2500, 3400], [-2000, 1400]]
ZADANE_FIALOVE = [[4500, 4400], [4100, 3000], [1800, 2400], [2500, 3400], [2000, 1400]]

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


def vizualizuj(matica):
    colors = ["white", "red", "green", "blue", "purple"]
    bounds = [BIELA, CERVENA, ZELENA, MODRA, FIALOVA, 5]
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    extent = [DOLNA_HRANICA, HORNA_HRANICA, DOLNA_HRANICA, HORNA_HRANICA]
    plt.imshow(matica, interpolation="none", cmap=cmap, norm=norm, extent=extent, origin="lower")

    # plt.show()
    nazov = casova_pecat(".png", str(ROZMER_MATICE)+"-test-vizualizacie")
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
    matica[yy][xx] = farba
    # print("Do matice bol vlozeny bod", x, y, farba)


def prenasob_suradnice():
    pomocne_cervene = []
    pomocne_zelene = []
    pomocne_modre = []
    pomocne_fialove = []

    for i in range(5):
        pomocne_cervene.append([ZADANE_CERVENE[i][0]//KOEFICIENT, ZADANE_CERVENE[i][1]//KOEFICIENT])
        pomocne_zelene.append([ZADANE_ZELENE[i][0]//KOEFICIENT, ZADANE_ZELENE[i][1]//KOEFICIENT])
        pomocne_modre.append([ZADANE_MODRE[i][0]//KOEFICIENT, ZADANE_MODRE[i][1]//KOEFICIENT])
        pomocne_fialove.append([ZADANE_FIALOVE[i][0]//KOEFICIENT, ZADANE_FIALOVE[i][1]//KOEFICIENT])

    print(pomocne_cervene)
    print(pomocne_zelene)
    print(pomocne_modre)
    print(pomocne_fialove)

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


def main():
    """Hlavna funkcia programu
    
    :return: 
    """
    zaciatok_funkcie(main.__name__, True)

    generovanie_matice_start = time.time()
    matica = vytvor_maticu()
    generovanie_matice_end = time.time()
    print("Generovanie matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                  generovanie_matice_end - generovanie_matice_start))

    vloz_povodnych_20(matica)
    # zrataj_pocet_bodov(matica)
    vykresli_hranice(matica)
    # zrataj_pocet_bodov(matica)

    # x, y = prerataj_suradnice(-10, -0)
    # vloz_do_matice(matica, x, y, CERVENA)
    # for y in range(-50, 51):
    #     for x in range(-50, 51):
    #         xx, yy = prerataj_suradnice(x, y)
    #         farba = CERVENA if y % 2 == 0 else MODRA
    #         vloz_do_matice(matica, x, y, farba)

    vizualizacia_start = time.time()
    vizualizuj(matica)
    vizualizacia_end = time.time()
    print("Vizualizacia matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                   vizualizacia_end - vizualizacia_start))

    # plt.matshow(matica)
    # plt.colorbar()
    # plt.show()

    # vizualizacia_start = time.time()
    # vizualizuj_zla(matica, ROZMER_MATICE)
    # vizualizacia_end = time.time()
    # print("Vizualizacia matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE, vizualizacia_end-vizualizacia_start))



    zaciatok_funkcie(main.__name__, False)


if __name__ == "__main__":
    main()
