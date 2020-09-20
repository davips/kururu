from akangatu.dataindependent import DataIndependent
from transf.absdata import AbsData


class DelIn(DataIndependent):
    def _transform_(self, data: AbsData):
        return data.replace(self, inner=None)

    def _config_(self):
        return {}
