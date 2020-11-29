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
#
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
#

from abc import ABC, abstractmethod

from akangatu.ddstep import DDStep
from transf.config import globalcache


class Sampler(DDStep, ABC):
    """Base class for Step classes that have a resample method, e.g., PCA and resampling (currently only X,y)."""

    def __init__(self, **config):
        super().__init__(**config)

    def _process_(self, data):
        matrices = {"X": lambda: self.sampled(data.inner)[0],
                    "Y": lambda: self.sampled(data.inner)[1]}
        return data.update(self, **matrices)

    @globalcache
    def sampled(self, data):
        """Sampled version of matrices.

        This cached method is needed because more than one matrix is calculated lazily inside process()."""
        return self.model(data.inner).resample(*data.Xy)

    @globalcache
    def model(self, data):
        """Sampler based on the training set..

        This cached method is needed because the so called "model" is called more than once inside process()."""
        model = self.algorithm
        model.fit(*data.Xy)
        return model

    @property
    def algorithm(self):
        return self._algorithm_func()()

    @abstractmethod
    def _algorithm_func(self):
        pass
