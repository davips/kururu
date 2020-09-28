import numpy as np
from sklearn.metrics import accuracy_score

from akangatu.distep import DIStep
from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.evaluation.mixin.functioninspection import withFunctionInspection
from transf.absdata import AbsData


class Metric(DIStep, withFunctionInspection):
    """Metric over a field.

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

    def __init__(self, functions=None, target="Y", prediction="Z"):
        if functions is None:
            functions = ["accuracy"]
        self.functions = functions
        self.target, self.prediction = target, prediction
        self.selected = [self.function_from_name[name] for name in functions]
        config = {"functions": functions, "target": target, "prediction": prediction}
        super().__init__(config)

    def _process_(self, data: AbsData):
        newr = np.array([f(data, self.target, self.prediction) for f in self.selected])
        return data.replace(self, r=newr)

    @staticmethod
    def _fun_error(data, target, prediction):
        return 1 - accuracy_score(data.field(target, "metric"), data.field(prediction, "metric"))

    @staticmethod
    def _fun_accuracy(data, target, prediction):
        return accuracy_score(data.field(target, "metric"), data.field(prediction, "metric"))

    @staticmethod
    def _fun_history(data, target, prediction):
        return len(list(data.history))


class Metric2(asMacro, Metric):
    def _step_(self):
        return Metric(**self.held) * In(Metric(**self.held))
