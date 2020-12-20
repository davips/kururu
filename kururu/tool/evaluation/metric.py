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
from sklearn.metrics import accuracy_score

from aiuna.content.data import Data
from akangatu.abs.mixin.macro import asMacro
from akangatu.distep import DIStep
from akangatu.operator.unary.inop import In
from akangatu.transf.mixin.config import asUnitset
from kururu.tool.evaluation.mixin.functioninspection import withFunctionInspection


class Metrico(asUnitset, DIStep, withFunctionInspection):
    """Metric over fields.

    Only the-higher-the-better functions in Metric, but can be negated:
    '-accuracy' -> 'accuracy' * -1

    Developer: new metrics can be added just by following the pattern '_fun_xxxxx'
    where xxxxx is the name of the new metric.

    Parameters
    ----------
    functions
        Name of the function to use to evaluate data objects.
    target
        Name of the matrix with expected values.
    prediction
        Name of the matrix to be measured.
    """

    # noinspection PyDefaultArgument
    def __init__(self, functions=["accuracy"], target="Y",
                 prediction="Z"):  # TODO:change all default prameters to "mutable"
        super().__init__(functions=functions, target=target, prediction=prediction)
        self.functions = functions
        self.target, self.prediction = target, prediction
        self.selected = [self.function_from_name[name] for name in functions]

    def _process_(self, data: Data):
        newr = lambda: np.array([f(data, self.target, self.prediction) for f in self.selected])
        return data.update(self, r=newr)

    @staticmethod
    def _fun_accuracy(data, target, prediction):
        return accuracy_score(data[target], data[prediction])

    @staticmethod
    def _fun_history(data, target, prediction):
        return -len(list(data.history))


metric = Metrico


class Metricb(asMacro, Metrico):
    def _step_(self):
        metric = Metrico(**self.held)
        return metric * In(metric)
