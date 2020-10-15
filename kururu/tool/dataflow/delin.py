from aiuna.content.data import Data
from akangatu.distep import DIStep
from transf.mixin.config import asConfigLess


class DelIn(asConfigLess, DIStep):
    def _process_(self, data: Data):
        return data.update(self, inner=None)

