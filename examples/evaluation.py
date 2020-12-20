# Evaluated training

from aiuna import *
from kururu import *

d = dataset("abalone").data

# Each imported step is a callable object which can be used with no parameters.
steps = binarize * split * pca * svm * metric

# After the Data object goes through the steps, its last version has the test accuracy value at 'r'.
d2 = d >> steps
print(d2.r)
# ...
