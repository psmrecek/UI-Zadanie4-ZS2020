#!/usr/bin/env python3.8
import time

ROZMER_MATICE = 10001
POLOVICA_ROZMERU = ROZMER_MATICE // 2
HORNA_HRANICA = POLOVICA_ROZMERU
DOLNA_HRANICA = -POLOVICA_ROZMERU
OHRANICENIE = POLOVICA_ROZMERU // 10
KOEFICIENT = 10000 // (ROZMER_MATICE - 1)


def vytvor_maticu():
    matica = [[0 for i in range(ROZMER_MATICE)] for j in range(ROZMER_MATICE)]
    return matica

def prerataj_suradnice(x, y):
    x_matica = x + POLOVICA_ROZMERU
    y_matica = y + POLOVICA_ROZMERU

    return x_matica, y_matica

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

def vyfarbi_mapu(matica):
    for x in range(DOLNA_HRANICA, HORNA_HRANICA + 1):
        for y in range(DOLNA_HRANICA, HORNA_HRANICA + 1):
            farba = ziskaj_farbu_z_matice(matica, x, y)
            if farba == 0:
                vloz_do_matice(matica, x, y, 1)

generovanie_matice_start = time.time()
matica = vytvor_maticu()
generovanie_matice_end = time.time()
print("Generovanie matice velkosti {}x{} zabralo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                              generovanie_matice_end - generovanie_matice_start))

vyfarbenie_mapy_star = time.time()
vyfarbi_mapu(matica)
vyfarbenie_mapy_end = time.time()
print("Vyfarbenie matice {}x{} trvalo {} s".format(ROZMER_MATICE, ROZMER_MATICE,
                                                                           vyfarbenie_mapy_end - vyfarbenie_mapy_star))