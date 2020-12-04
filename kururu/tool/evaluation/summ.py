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

from numpy import mean, array

from akangatu import linalghelper
from akangatu.abs.mixin.macro import asMacro
from akangatu.distep import DIStep
from akangatu.fieldchecking import Forbid
from kururu.tool.evaluation.mixin.functioninspection import withFunctionInspection
from kururu.tool.manipulation.copy_ import Copy
from kururu.tool.stream.internal.accumulator import Accumulator
from akangatu.abs.mixin.fixedparam import asFixedParam


class Summ(asFixedParam, DIStep, withFunctionInspection):
    # Yes, we use "mutable" defaults because (it is immutable here and) better to show what to expect from the method.
    # ...and lists are more confortable to write/read than tuples.
    # noinspection PyDefaultArgument
    def __init__(self, stage="test", field="R", functions=["mean"]):
        super().__init__(stage=stage, field=field, functions=functions)
        self.functions = functions
        self.selected = [self.function_from_name[name] for name in functions]
        self.field = field
        if stage not in ["train", "test"]:
            print("Unknown stage:", stage)
            exit()
        self.stage = stage

    def _process_(self, data):
        if data.stream is None:
            print(f"{self.name} needs a Data object containing a stream.")
            print("Missing stream inside", data.id)
            exit()

        def step_func(data_, acc):
            if self.stage == "train":
                v = data_.inner.field(self.field, context=self)
            else:
                v = data_.field(self.field, context=self)
            return {"data": data_, "inc": linalghelper.mat2vec(v)}

        def end_func(acc):
            return [array(f(acc)) for f in self.selected]

        iterator = Accumulator(lambda: data.stream, start=[], step_func=step_func, end_func=end_func)
        return data.update(self, stream=lambda: iterator, S=lambda: iterator.result)

    @staticmethod
    def _fun_mean(values):
        return mean(values, axis=0)


class Summ2(asMacro, Summ):
    def _step_(self):
        train = Summ(stage="train", **self.held)
        test = Summ(stage="test", **self.held)
        return Forbid("inner") * train * Copy("S", "Si") * test

    # REMINDER: loop infinito no uuid ou json pode indicar presença de classe no config
