from aiuna.delete import Del
from akangatu.distep import DIStep
from akangatu.innerchecking import EnsureNoInner
from transf.mixin.config import asConfigLess


class AutoIns(asConfigLess, DIStep):
    def _process_(self, data):
        EnsureNoInner().process(data)
        inner = lambda: Del("stream").process(data)  # blank stream to avoid confusion with two pointers to the same iterator
        return data.update(self, inner=inner)
