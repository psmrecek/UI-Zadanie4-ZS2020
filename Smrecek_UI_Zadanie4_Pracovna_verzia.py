import matplotlib.pyplot as plt
import matplotlib as mpl
import time

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

ROZMER_MATICE = 1001
POLOVICA_ROZMERU = ROZMER_MATICE // 2
HORNA_HRANICA = POLOVICA_ROZMERU
DOLNA_HRANICA = -POLOVICA_ROZMERU

OHRANICENIE = POLOVICA_ROZMERU // 10


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


def vizualizuj_zla(matica, rozmer_matice):
    plt.xlim(DOLNA_HRANICA, HORNA_HRANICA)
    plt.ylim(DOLNA_HRANICA, HORNA_HRANICA)

    for i in range(rozmer_matice):
        for j in range(rozmer_matice):
            trieda = matica[i][j]
            farba = None
            if trieda == b"R":
                farba = "ro"
            elif trieda == b"B":
                farba = "bo"
            elif trieda == b"G":
                farba = "go"
            elif trieda == b"P":
                farba = "mo"
            elif trieda == b"W":
                farba = "wo"
            else:
                print("Neznama farba", i, j, trieda)

            # plt.plot(i - POLOVICA_ROZMERU, j - POLOVICA_ROZMERU, farba)

    plt.show()


def vizualizuj(matica):
    colors = ['white', 'red', 'green', 'blue', 'purple']
    bounds = [0, 1, 2, 3, 4, 5]
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    extent = [DOLNA_HRANICA, HORNA_HRANICA, DOLNA_HRANICA, HORNA_HRANICA]
    plt.imshow(matica, interpolation='none', cmap=cmap, norm=norm, extent=extent, origin="lower")

    plt.show()


def vytvor_maticu(rozmer_matice):
    # riadok = [b"w" for i in range(rozmer_matice)]
    matica = [[0 for i in range(rozmer_matice)] for j in range(rozmer_matice)]
    # print("Skoncilo generovanie")
    # vypis(matica)
    polovica_rozmeru = rozmer_matice // 2

    # x_matica, y_matica = suradnice(-5, -5, rozmer_matice)
    # matica[x_matica][y_matica] = b"O"
    # x_matica, y_matica = suradnice(-5, -5, rozmer_matice)
    # matica[x_matica][y_matica] = b"O"
    # for i in range(-5, 0):
    #     for j in range(-5, 0):
    #         x, y = suradnice(i, j, rozmer_matice)
    #         if matica[x][y] != b"W":
    #             print("CHYBA")
    #             return
    #         matica[x][y] = b"R"
    #         # matica[i][j] = b"R"
    #
    # for i in range(1, 6):
    #   for j in range(1, 6):
    #         x, y = suradnice(i, j, rozmer_matice)
    #         if matica[x][y] != b"W":
    #             print("CHYBA")
    #             return
    #         matica[x][y] = b"P"
    #         # matica[i][j] = b"P"
    #
    # for i in range(-5, 0):
    #   for j in range(1, 6):
    #         x, y = suradnice(i, j, rozmer_matice)
    #         if matica[x][y] != b"W":
    #             print("CHYBA")
    #             return
    #         matica[x][y] = b"B"
    #         # matica[i][j] = b"B"
    #
    # for i in range(1, 6):
    #   for j in range(-5, 0):
    #         # x, y = suradnice(i, j, rozmer_matice)
    #         if matica[x][y] != b"W":
    #             print("CHYBA")
    #             return
    #         matica[x][y] = b"G"
    #         # matica[i][j] = b"G"

    # print(polovica_rozmeru)

    for i in range(0, polovica_rozmeru + OHRANICENIE):
        for j in range(0, polovica_rozmeru + OHRANICENIE):
            # matica[i][j] = b"R"
            matica[i][j] = 1

    for i in range(0, polovica_rozmeru + OHRANICENIE):
        for j in range(polovica_rozmeru - OHRANICENIE, rozmer_matice):
            # matica[i][j] = b"G"
            matica[i][j] = 2

    for i in range(polovica_rozmeru - OHRANICENIE, rozmer_matice):
        for j in range(0, polovica_rozmeru + OHRANICENIE):
            # matica[i][j] = b"B"
            matica[i][j] = 3

    for i in range(polovica_rozmeru - OHRANICENIE, rozmer_matice):
        for j in range(polovica_rozmeru - OHRANICENIE, rozmer_matice):
            # matica[i][j] = b"P"
            matica[i][j] = 4

    # vypis(matica)
    return matica


def main():
    """Hlavna funkcia programu
    
    :return: 
    """
    zaciatok_funkcie(main.__name__, True)

    # plt.plot([1, 2, 3, 4])
    # plt.ylabel('some numbers')
    # plt.show()

    generovanie_matice_start = time.time()
    matica = vytvor_maticu(ROZMER_MATICE)
    generovanie_matice_end = time.time()
    print("Generovanie matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE, generovanie_matice_end-generovanie_matice_start))

    # plt.matshow(matica)
    # plt.colorbar()
    # plt.show()


    # vizualizacia_start = time.time()
    # vizualizuj_zla(matica, ROZMER_MATICE)
    # vizualizacia_end = time.time()
    # print("Vizualizacia matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE, vizualizacia_end-vizualizacia_start))

    vizualizacia_start = time.time()
    vizualizuj(matica)
    vizualizacia_end = time.time()
    print("Vizualizacia matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE, vizualizacia_end-vizualizacia_start))


    zaciatok_funkcie(main.__name__, False)


if __name__ == "__main__":
    main()