# Creating a custom step
from akangatu.distep import DIStep


# DIStep means "Data Independent Step", i.e. it does not depend on previously known data.
class MyAdditionStep(DIStep):
    """Multiplies the given field by a factor."""

    def __init__(self, field, factor):
        # All relevant step parameters should be passed to super() as keyword arguments.
        super().__init__(field=field, factor=factor)

        # Instance attributes are set as usual.
        self.field = field
        self.factor = factor

    def _process_(self, data):
        # All calculations (including access to data fields)
        #   is deferred to a future access to the return field - R in this case.
        return data.update(self, R=lambda: data[self.field] * self.factor)
