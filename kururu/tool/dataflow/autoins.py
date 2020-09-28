from akangatu import Ins
from akangatu.distep import DIStep
from transf.step import Step


class AutoIns(DIStep):
    def __init__(self):
        super().__init__({})

    def _process_(self, data):
        # return Step.makeupuuid(Ins(), self.uuid).process(data)
        return Step.makeupuuid(Ins(data), self.uuid).process(data)

