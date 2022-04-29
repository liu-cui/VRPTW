import numpy as np
import matplotlib.pyplot as plt


rnd = np.random
rnd.seed(0)

n = 20  # numbre of clients
xc = rnd.rand(n+1)*200
yc = rnd.rand(n+1)*100
plt.plot(xc[0], yc[0], c='r', marker='s')
plt.scatter(xc[1:], yc[1:], c='b')
plt.show()