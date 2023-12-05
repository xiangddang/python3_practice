import numpy as np

# version of numpy
print(np.__version__)

# create a 1D array
arr = np.arange(10)
print(arr)

# create a boolean array
arr = np.full((3, 3), True, dtype=bool)
print(arr)