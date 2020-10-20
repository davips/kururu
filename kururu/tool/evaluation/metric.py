import numpy as np
from aiuna.content.data import Data
from sklearn.metrics import accuracy_score

from akangatu.distep import DIStep
from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.evaluation.mixin.functioninspection import withFunctionInspection
from transf.mixin.config import asUnitset


class Metric(asUnitset, DIStep, withFunctionInspection):
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
    def __init__(self, functions=["accuracy"], target="Y", prediction="Z"):  # TODO:change all default prameters to "mutable"
        super().__init__(functions=functions,target=target,prediction=prediction)
        self.functions = functions
        self.target, self.prediction = target, prediction
        self.selected = [self.function_from_name[name] for name in functions]

    def _process_(self, data: Data):
        newr = lambda: np.array([f(data, self.target, self.prediction) for f in self.selected])
        return data.update(self, r=newr)

    @staticmethod
    def _fun_accuracy(data, target, prediction):
        return accuracy_score(data.field(target, context="Metric"), data.field(prediction, context="Metric"))

    @staticmethod
    def _fun_history(data, target, prediction):
        return -len(list(data.history))


class Metric2(asMacro, Metric):
    def _step_(self):
        metric = Metric(**self.held)
        return metric * In(metric)
