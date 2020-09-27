from akangatu import Ins
from akangatu.distep import DIStep
from transf.step import Step


class AutoIns(DIStep):
    def _process_(self, data):
        # return Step.makeupuuid(Ins(), self.uuid).process(data)
        return Step.makeupuuid(Ins(data), self.uuid).process(data)

    def _config_(self):
        return {}
