from akangatu.distep import DIStep
from akangatu.innerchecking import EnsureNoInner
from kururu.tool.dataflow.delstream import DelStream
from transf.mixin.config import asConfigLess


class AutoIns(asConfigLess, DIStep):
    def _process_(self, data):
        EnsureNoInner().process(data)
        inner = DelStream().process(data)  # blank stream to avoid confusion
        return data.replace(self, inner=inner)

    # return Step.makeupuuid(Insert(data), self.uuid).process(data) # TODO: analisar se isso era necessario
