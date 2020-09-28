from numpy import mean, array

from aiuna.mixin import linalghelper
from akangatu.abs.mixin.macro import asMacro
from akangatu.distep import DIStep
from akangatu.innerchecking import EnsureNoInner
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.evaluation.mixin.functioninspection import withFunctionInspection
from kururu.tool.stream.accumulator import Accumulator
from transf.absdata import AbsData


# REMINDER: Summ é como o Split1 que sempre processa o dado em que é aplicado (ora como treino, ora como teste;
# mudado por parâmetro),
# distinto de PCA/SVM que são como Split, mas sempre esperam um dado interno (até dentro do interno) e não dependem
# do parâmetro que caracteriza o tipo de produção (treino ou teste).
# Assim, Summ representa dois passos distintos: ISumm e OSumm.

class Summ(DIStep, withFunctionInspection):
    # Yes, we use "mutable" defaults because (it is immutable here and) better to show what to expect from the method.
    # ...and lists are more confortable to write/read than tuples.
    # noinspection PyDefaultArgument
    def __init__(self, field="R", functions=["mean"]):
        super().__init__({"field": field, "functions": functions})
        self.functions = functions
        self.selected = [self.function_from_name[name] for name in functions]
        self.field = field

    def _process_(self, data: AbsData):
        if data.stream is None:
            print(f"{self.name} needs a Data object containing a stream.")
            print("Missing stream inside", data.id)
            exit()

        def step_func(data_, acc):
            print("fffffffffff", data_.field(self.field, context=self).shape)
            return data_, linalghelper.mat2vec(data_.field(self.field, context=self))

        def end_func(acc):
            return [array(f(acc)) for f in self.selected]

        iterator = Accumulator(data.stream, start=[], step_func=step_func, end_func=end_func)
        return data.replace(self, stream=iterator, S=lambda: iterator.result)

    @staticmethod
    def _fun_mean(values):
        return mean(values, axis=0)


class Summ2(asMacro, Summ):
    def _step_(self):
        external = Summ(**self.held)
        internal = In(Summ(**self.held))
        return EnsureNoInner * AutoIns * external * internal
