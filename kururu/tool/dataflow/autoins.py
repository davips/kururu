from akangatu.distep import DIStep
from akangatu.innerchecking import EnsureNoInner
from kururu.tool.dataflow.delstream import DelStream
from transf.mixin.config import asConfigLess


class AutoIns(asConfigLess, DIStep):
    def _process_(self, data):
        EnsureNoInner().process(data)
        inner = DelStream().process(data)  # blank stream to avoid confusion with two pointers to the same iterator
        return data.update(self, inner=inner)
