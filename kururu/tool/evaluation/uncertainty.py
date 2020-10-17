from akangatu.distep import DIStep
from transf.absdata import AbsData
from transf.mixin.config import asConfigLess


class Margin(asConfigLess, DIStep):
    def _process_(self, data: AbsData):
        P = data.field("P", context=self).copy()
        P.sort()
        U = P[:, 1] - P[:, 0]
        # print(P.shape, U.shape)
        return data.update(self, U=U)


class Entropy(asConfigLess, DIStep):
    def _process_(self, data: AbsData):
        raise NotImplemented
