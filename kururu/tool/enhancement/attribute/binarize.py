#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the kururu project.
#  Please respect the license - more about this in the section (*) below.
#
#  kururu is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  kururu is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

import numpy as np
from sklearn.preprocessing import OneHotEncoder

from aiuna.content.data import Data
from aiuna.content.creation import nominal_idxs
from akangatu.distep import DIStep
from akangatu.transf.mixin.config import asConfigLess


class Binarize(asConfigLess, DIStep):  # TODO: other fields
    """Convert each nominal attribute to numeric ones by one-hot-encoding.

    All distinct values should be known before hand.
    There is no distinction between training and testing parts of the dataset.
    [this can be improved in the future by inheriting Transformer]

    For conversion from continuous attributes to binary attributes
    (same effect as nominal with two values) see step Discretize."""

    def _process_(self, data: Data):
        # REMINDER: Binarize will do nothing to numeric datasets, but the uuid still needs to be predictable.
        # So, the provided Data object should be "processed" anyway.
        def func():
            data_nominal_idxs = nominal_idxs(data.Xt)
            encoder = OneHotEncoder()
            if len(data_nominal_idxs) > 0:
                nom = encoder.fit_transform(data.X[:, data_nominal_idxs]).toarray()
                num = np.delete(data.X, data_nominal_idxs, axis=1).astype(float)
                return np.column_stack((nom, num))
            return data.X

        return data.update(self, X=func)


binarize = Binarize()
