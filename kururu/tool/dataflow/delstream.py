from aiuna.content.data import Data
from akangatu.distep import DIStep
from transf.mixin.config import asConfigLess


class DelStream(asConfigLess, DIStep):
    def _process_(self, data: Data):
        return data.update(self, stream=None)

# TODO : Lift()   stream from inner to outer.
#  Lembrar da inspiração em monads pra embutir dado dentro de outro e fazer operações infiltradas para art.
