from itertools import repeat

from akangatu.container import Container1
from transf.absdata import AbsData
from transf.mixin.streamhandler import asStreamHandler


class Map(asStreamHandler, Container1):
    def _workers_(self):
        return repeat(self.step)

    def _process_(self, data: AbsData):
        print("começa map")
        if data.stream is None:
            print(f"{self.name} needs a Data object containing a stream.")
            print("Missing stream inside", data.id)
            exit()
        return data.replace(self, stream=map(self.step.process, data.stream))
