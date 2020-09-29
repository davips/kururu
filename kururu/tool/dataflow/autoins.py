from akangatu.innerchecking import EnsureNoInner
from akangatu import Insert
from akangatu.distep import DIStep
from kururu.tool.dataflow.delstream import DelStream
from transf.step import Step


class AutoIns(DIStep):
    def __init__(self):
        super().__init__({})

    def _process_(self, data):
        EnsureNoInner().process(data)
        inner = DelStream().process(data)  # blank stream to avoid confusion
        return data.replace(self, inner=inner)

    # return Step.makeupuuid(Insert(data), self.uuid).process(data) # TODO: analisar se isso era necessario
