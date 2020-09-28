from sklearn.svm import NuSVC

from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.dataflow.delin import DelIn
from kururu.tool.learning.supervised.abs.predictor import Predictor


class SVM(Predictor):
    """  """

    def __init__(self, inner=None, **kwargs):  # TODO :params and defaults
        super().__init__(inner, config=kwargs)

    def _model_(self, data):
        nusvc = NuSVC(**self.config)
        nusvc.fit(*data.Xy)
        return nusvc


class SVM2(asMacro, SVM):
    def _step_(self):
        return SVM(**self.held) * In(AutoIns * SVM(**self.held) * DelIn)

    # x = 0.00001
    # l = []
    # for i in range(128):
    #     x = x * 1.1
    #     l.append(x)
    # print(l)
