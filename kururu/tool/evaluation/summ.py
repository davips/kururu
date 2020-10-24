from numpy import mean, array

import linalghelper
from akangatu.abs.mixin.macro import asMacro
from akangatu.distep import DIStep
from akangatu.innerchecking import EnsureNoInner
from kururu.tool.evaluation.mixin.functioninspection import withFunctionInspection
from kururu.tool.manipulation.copy import Copy
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
        return EnsureNoInner * train * Copy("S", "Si") * test

    # REMINDER: loop infinito no uuid ou json pode indicar presença de classe no config
