from akangatu.distep import DIStep
from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from akangatu.innerchecking import EnsureNoInner
from kururu.tool.evaluation.mixin.partitioning import withPartitioning
from transf.absdata import AbsData


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
            print("Unknown stage:",stage)
            exit()

        withPartitioning.__init__(self, mode, config)
        DIStep.__init__(self, config)

    def _process_(self, data: AbsData):
        if self._indices is None:
            self._indices = self.partitionings(data)[self.i][self.istep]

        newmatrices = {}
        for f in self.fields:
            newmatrices[f] = data.field(f, context=self)[self._indices]
        return data.replace(self, **newmatrices)


class Split(withPartitioning, asMacro, DIStep):
    def __init__(self, i=0, mode="holdout", splits=2, test_size=0.3, seed=0, fields="X,Y", _indices=None):
        config = locals().copy()
        del config["self"]
        del config["_indices"]
        withPartitioning.__init__(self, mode, config)
        DIStep.__init__(self, config)

    def _step_(self):
        # print("held:", self.held)
        internal = In(Split1(stage="train", **self.held))
        external = Split1(stage="test", **self.held)
        return EnsureNoInner * AutoIns * external * internal
