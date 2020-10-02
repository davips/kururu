from akangatu.distep import DIStep
from transf.absdata import AbsData


class Margin(DIStep):
    def _process_(self, data: AbsData):
        return data.replace(self, U=data.Y - data.Z)
