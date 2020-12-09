import numpy as np
import matplotlib.pyplot as plt
from kdtrees import KDTree

# ROZMER_MATICE = 2
#
# matica = [[0 for i in range(ROZMER_MATICE)] for j in range(ROZMER_MATICE)]

tree = KDTree.initialize([[1, 2], [2, 3], [-10, -3]])
tree.insert([0, 0])

susedia = tree.nearest_neighbor([0, 1], n=20)

print(susedia)



# tree.visualize()

