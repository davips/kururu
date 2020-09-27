from _ast import In
from functools import lru_cache

from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold, LeaveOneOut

from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.evaluation.mixin.partitioning import withPartitioning
from kururu.tool.evaluation.split import Split1
from akangatu.distep import DIStep
from transf.absdata import AbsData


class Partition(withPartitioning, DIStep):
    def __init__(self, mode="cv", splits=10, test_size=0.3, seed=0, fields="X,Y"):
        config = locals().copy()
        del config["self"]
        del config["__class__"]
        super().__init__(mode, config)

    def _process_(self, data: AbsData):
        """"""
        idxs = self.partitionings(data)

        # REMINDER: Partition faz data virar data com stream; e nesse stream vem data transformado e com inner.
        def gen():
            for i in range(self.splits):
                trainS = Split1(i, "train", **self.config, _indices=idxs[i][0])
                testS = Split1(i, "test", **self.config, _indices=idxs[i][1])
                wk = AutoIns * In(trainS) * testS
                yield wk.process(data)

        return data.replace(self, stream=gen())
