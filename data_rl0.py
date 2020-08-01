import os
import numpy as np
from PIL import Image

dt =np.dtype(np.int16)
l= np.fromfile('black.rl0', dtype=dt).reshape((8238,6000))
np.save("black_numpy",l)