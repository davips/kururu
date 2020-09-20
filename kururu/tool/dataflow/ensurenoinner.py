from akangatu.dataindependent import DataIndependent
from transf.absdata import AbsData


class EnsureNoInner(DataIndependent):
    def _transform_(self, data: AbsData):
        if data.inner:
            raise Exception("Cannot proceed with inner data!", data)
        return data

    def _config_(self):
        return {}
