from akangatu.distep import DIStep
from transf.absdata import AbsData


class DelStream(DIStep):
    def __init__(self):
        super().__init__({})

    def _process_(self, data: AbsData):
        return data.replace(self, stream=None)

# TODO : Lift()   stream from inner to outer.
#  Lembrar da inspiração em monads pra embutir dado dentro de outro e fazer operações infiltradas para art.
