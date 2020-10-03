from akangatu.distep import DIStep
from transf.absdata import AbsData
from akangatu.abs.mixin.paramless import asParamLess


class Margin(asParamLess, DIStep):
    def _process_(self, data: AbsData):
        P = data.field("P", context=self).copy()
        P.sort()
        U = P[:, 1] - P[:, 0]
        print(P.shape, U.shape)
        return data.replace(self, U=U)


class Entropy(asParamLess, DIStep):
    def _process_(self, data: AbsData):
        raise NotImplemented
