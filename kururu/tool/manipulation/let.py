from akangatu.distep import DIStep
from transf.absdata import AbsData


class Let(DIStep):
    def __init__(self, field="V", value=True):
        super().__init__({"field": field, "value": value})

    def _process_(self, data: AbsData):
        dic = {self.field: self.value}
        return data.update(self, **dic)
