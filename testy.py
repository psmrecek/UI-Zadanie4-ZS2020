import numpy as np
import matplotlib.pyplot as plt
from kdtrees import KDTree

# ROZMER_MATICE = 2
#
# matica = [[0 for i in range(ROZMER_MATICE)] for j in range(ROZMER_MATICE)]

pole = []
for i in range(20020):
    pole.append([i, i+1])

# print(pole)

strom = KDTree.initialize(pole)
susedia = strom.nearest_neighbor([0, 2], n=20)

print(susedia)

# tree = KDTree.initialize([[0, 1]])
#
#
# for i in range(0, 2000):
#     tree.insert([0, -i])
#     print("Vlozil som bod ", i + 1)
#
# print("SKONCILO NAHRAVANIE")
#
# susedia = tree.nearest_neighbor([0, 2], n=20)
#
# print(susedia)



# tree.visualize()

