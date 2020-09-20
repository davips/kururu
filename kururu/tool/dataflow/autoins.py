from akangatu import Ins
from akangatu.dataindependent import DataIndependent
from transf.transformer import Transformer


class AutoIns(DataIndependent):
    def _transform_(self, data):
        return Transformer.makeupuuid(Ins(data), self.uuid).transform(data)

    def _config_(self):
        return {}
