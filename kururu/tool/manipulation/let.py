from akangatu.distep import DIStep
class Let(DIStep):
    def __init__(self, field="V", value=True):
        super().__init__(field=field, value=value)

    def _process_(self, data):
        dic = {self.field: self.value}
        return data.update(self, **dic)
