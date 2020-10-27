from aiuna.content.data import Data
from akangatu.distep import DIStep
from akangatu.abs.mixin.macro import asMacro
from akangatu.fieldchecking import Forbid
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.evaluation.mixin.partitioning import withPartitioning


class Split1(DIStep, withPartitioning):
    """  """

    def __init__(self, i=0, stage="test", mode="holdout", splits=2, test_size=0.3, seed=0, fields="X,Y", _indices=None):
        config = locals().copy()
        del config["self"]
        del config["_indices"]
        self._indices = _indices
        self.i = i
        if stage == "train":
            self.istep = 0
        elif stage == "test":
            self.istep = 1
        else:
            print("Unknown stage:", stage)
            exit()

        withPartitioning.__init__(self, mode, config)
        DIStep.__init__(self, **config)

    def _process_(self, data: Data):
        def indices():
            if self._indices is None:
                self._indices = self.partitionings(data)[self.i][self.istep]
            return self._indices

        newmatrices = {}
        for f in self.fields:
            newmatrices[f] = (lambda f: lambda: data[f][indices()])(f)
        return data.update(self, **newmatrices)


class Split(withPartitioning, asMacro, DIStep):
    def __init__(self, i=0, mode="holdout", splits=2, test_size=0.3, seed=0, fields="X,Y", _indices=None):
        config = locals().copy()
        del config["self"]
        del config["_indices"]
        withPartitioning.__init__(self, mode, config)
        DIStep.__init__(self, **config)

    def _step_(self):
        # print("held:", self.held)
        internal = In(Split1(stage="train", **self.held))
        external = Split1(stage="test", **self.held)
        return Forbid("inner") * AutoIns * external * internal
