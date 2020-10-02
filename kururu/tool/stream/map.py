from akangatu.container import Container1
from transf.absdata import AbsData


class Map(Container1):

    def _process_(self, data: AbsData):
        if data.stream is None:
            print(f"{self.name} needs a Data object containing a stream.")
            print("Missing stream inside", data.id)
            exit()
        return data.replace(self, stream=map(self.step.process, data.stream))
