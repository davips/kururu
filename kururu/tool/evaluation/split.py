#  Copyright (c) 2020. Davi Pereira dos Santos
#      This file is part of the kururu project.
#      Please respect the license. Removing authorship by any means
#      (by code make up or closing the sources) or ignoring property rights
#      is a crime and is unethical regarding the effort and time spent here.
#      Relevant employers or funding agencies will be notified accordingly.
#
#      kururu is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      kururu is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#

from aiuna.content.data import Data
from akangatu.distep import DIStep
from akangatu.abs.mixin.macro import asMacro
from akangatu.fieldchecking import Forbid
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.evaluation.mixin.partitioning import withPartitioning


class Split1(DIStep, withPartitioning):
    """  """

    def __init__(self, i=0, stage="test", mode="holdout", splits=2, test_size=0.3, seed=0, fields="X,Y", _indices=None):
        config = locals().copy()
        del config["self"]
        del config["_indices"]
        self._indices = _indices
        self.i = i
        if stage == "train":
            self.istep = 0
        elif stage == "test":
            self.istep = 1
        else:
            print("Unknown stage:", stage)
            exit()

        withPartitioning.__init__(self, mode, config)
        DIStep.__init__(self, **config)

    def _process_(self, data: Data):
        def indices():
            if self._indices is None:
                self._indices = self.partitionings(data)[self.i][self.istep]
            return self._indices

        newmatrices = {}
        for f in self.fields:
            newmatrices[f] = (lambda f: lambda: data[f][indices()])(f)
        return data.update(self, **newmatrices)


class Split(withPartitioning, asMacro, DIStep):
    def __init__(self, i=0, mode="holdout", splits=2, test_size=0.3, seed=0, fields="X,Y", _indices=None):
        config = locals().copy()
        del config["self"]
        del config["_indices"]
        withPartitioning.__init__(self, mode, config)
        DIStep.__init__(self, **config)

    def _step_(self):
        # print("held:", self.held)
        internal = In(Split1(stage="train", **self.held))
        external = Split1(stage="test", **self.held)
        return Forbid("inner") * AutoIns * external * internal
