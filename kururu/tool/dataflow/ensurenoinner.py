from akangatu.distep import DIStep
from transf.absdata import AbsData


class EnsureNoInner(DIStep):
    def _process_(self, data: AbsData):
        if data.inner:
            raise Exception("Cannot proceed with inner data!", data)
        return data

    def _config_(self):
        return {}
