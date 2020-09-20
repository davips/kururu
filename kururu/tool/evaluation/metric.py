import numpy as np
from sklearn.metrics import accuracy_score

from akangatu.dataindependent import DataIndependent
from kururu.tool.evaluation.mixin.functioninspection import withFunctionInspection
from transf.absdata import AbsData


class Metric(DataIndependent, withFunctionInspection):
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
        self._config = {"functions": functions, "target": target, "prediction": prediction}

    def _transform_(self, data: AbsData):
        newr = np.array([f(data, self.target, self.prediction) for f in self.selected])
        return data.replace(self, r=newr)

    def _config_(self):
        return self._config

    @staticmethod
    def _fun_error(data, target, prediction):
        return 1 - accuracy_score(data.field(target, "metric"), data.field(prediction, "metric"))

    @staticmethod
    def _fun_accuracy(data, target, prediction):
        return accuracy_score(data.field(target, "metric"), data.field(prediction, "metric"))

    @staticmethod
    def _fun_history(data, target, prediction):
        return len(list(data.history))
