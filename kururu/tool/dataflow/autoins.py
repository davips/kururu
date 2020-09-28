from akangatu import Insert
from akangatu.distep import DIStep
from transf.step import Step


class AutoIns(DIStep):
    def __init__(self):
        super().__init__({})

    def _process_(self, data):
        # Chain new (inner) stream before the outer stream. (Because only the outer can see the other)
        # Traversing the outer, will traverse the inner. <- PORCARIA
        def gen():
            for i in data.stream:  # data.stream == inner_stream
                yield i

        inner = data
        outer = data.replace(self, inner=inner, stream=data.stream and gen())
        return outer

    # return Step.makeupuuid(Insert(data), self.uuid).process(data) # TODO: analisar se isso era necessario
