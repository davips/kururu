from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.evaluation.mixin.partitioning import withPartitioning
from kururu.tool.evaluation.split import Split1
from akangatu.distep import DIStep
from transf.absdata import AbsData
from akangatu.abs.mixin.fixedparam import asFixedParam


class Partition(asFixedParam, withPartitioning, DIStep):
    def __init__(self, mode="cv", splits=10, test_size=0.3, seed=0, fields="X,Y"):
        config = locals().copy()
        del config["self"]
        withPartitioning.__init__(self, mode, config)
        DIStep.__init__(self, **config)

    def _process_(self, data: AbsData):
        """"""
        idxs = self.partitionings(data)

        # REMINDER: Partition faz data virar data com stream; e nesse stream vem data transformado e com inner.
        def gen():
            for i in range(self.splits):
                # print("partition", i, end="   ")
                trainS = Split1(i, "train", **self.config, _indices=idxs[i][0])
                testS = Split1(i, "test", **self.config, _indices=idxs[i][1])
                wk = AutoIns * In(trainS) * testS
                yield wk.process(data)
            print()

        return data.update(self, stream=gen())

