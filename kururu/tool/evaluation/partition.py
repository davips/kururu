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

from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.evaluation.mixin.partitioning import withPartitioning
from kururu.tool.evaluation.split import Split1
from akangatu.distep import DIStep
from akangatu.abs.mixin.fixedparam import asFixedParam


class Partition(asFixedParam, withPartitioning, DIStep):
    def __init__(self, mode="cv", splits=10, test_size=0.3, seed=0, fields="X,Y"):
        config = locals().copy()
        del config["self"]
        withPartitioning.__init__(self, mode, config)
        DIStep.__init__(self, **config)

    def _process_(self, data):
        """"""
        idxs_func = lambda: self.partitionings(data)

        # REMINDER: Partition faz data virar data com stream; e nesse stream vem data transformado e com inner.
        def gen():
            idxs = idxs_func()
            for i in range(self.splits):
                # print("partition", i, end="   ")
                trainS = Split1(i, "train", **self.config, _indices=idxs[i][0])
                testS = Split1(i, "test", **self.config, _indices=idxs[i][1])
                wk = AutoIns * In(trainS) * testS
                yield wk.process(data)

        return data.update(self, stream=gen)
