from akangatu.distep import DIStep
from transf.absdata import AbsData
from transf.mixin.config import asConfigLess


class DelIn(asConfigLess, DIStep):
    def _process_(self, data: AbsData):
        return data.update(self, inner=None)

