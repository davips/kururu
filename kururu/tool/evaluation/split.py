from akangatu.dataindependent import DataIndependent
from akangatu.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.dataflow.ensurenoinner import EnsureNoInner
from kururu.tool.evaluation.mixin.partitioning import withPartitioning
from transf.absdata import AbsData


class Split1(DataIndependent, withPartitioning):
    """  """

    def __init__(self, i=0, step="train", mode="cv", splits=10, test_size=0.3, seed=0, fields="X,Y", _indices=None):
        config = locals().copy()
        del config["self"]
        del config["__class__"]
        del config["_indices"]
        super().__init__(mode, config)
        self._indices = _indices
        self.i = i
        self.istep = 0 if step == "train" else 1

    def _transform_(self, data: AbsData):
        if self._indices is None:
            self._indices = self.partitionings(data)[self.i][self.istep]

        newmatrices = {}
        for f in self.fields:
            newmatrices[f] = data.field(f, self)[self._indices]
        return data.replace(self, **newmatrices)

    def _config_(self):
        return self._config


class Split(withPartitioning, asMacro, DataIndependent):
    def __init__(self, i=0, mode="cv", splits=10, test_size=0.3, seed=0, fields="X,Y", _indices=None):
        config = locals().copy()
        del config["self"]
        del config["__class__"]
        del config["_indices"]
        super().__init__(mode, config)

    def _transformer_(self):
        print(self.held)
        return EnsureNoInner * AutoIns * In(Split1(step="train", **self.held)) * Split1(step="test", **self.held)

