import numpy as np
from sklearn.preprocessing import OneHotEncoder

from aiuna.content.data import Data
from aiuna.creation import nominal_idxs
from akangatu.distep import DIStep


class Binarize(DIStep):  # TODO: other fields
    def __init__(self):
        super().__init__({})

    def _process_(self, data: Data):
        data_nominal_idxs = nominal_idxs(data.Xt)
        encoder = OneHotEncoder()
        newmatrices = {}
        if len(data_nominal_idxs) > 0:
            nom = encoder.fit_transform(data.field("X", context=self)[:, data_nominal_idxs]).toarray()
            num = np.delete(data.field("X", context=self), data_nominal_idxs, axis=1).astype(float)
            newmatrices["X"] = np.column_stack((nom, num))

        return data.replace(self, **newmatrices)
