from akangatu.distep import DIStep
from transf.absdata import AbsData


class DelIn(DIStep):
    def _process_(self, data: AbsData):
        return data.replace(self, inner=None)

    def _config_(self):
        return {}
