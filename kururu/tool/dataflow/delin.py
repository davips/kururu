from akangatu.distep import DIStep
from transf.absdata import AbsData


class DelIn(DIStep):
    def __init__(self):
        super().__init__({})

    def _process_(self, data: AbsData):
        return data.replace(self, inner=None)
