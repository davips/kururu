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

from sklearn.svm import SVC

from aiuna.delete import Del
from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.learning.supervised.abs.predictor import Predictor


class SVM(Predictor):
    """  """

    def __init__(self, inner=None, **kwargs):  # TODO :params and defaults
        super().__init__(inner, **kwargs)

    def _model_(self, data):
        nusvc = SVC(**self.config)
        nusvc.fit(*data.Xy)
        return nusvc


class SVM2(asMacro, SVM):
    def _step_(self):
        # print("svm hjhhhhhhhhhhhh", self.held)
        svm = SVM(**self.held)
        return svm * In(AutoIns * svm * Del("inner"))

# x = 0.00001
# l = []
# for i in range(28):
#     x = x * 1.777
#     l.append(x)
# print(max(l))
# print(l)
