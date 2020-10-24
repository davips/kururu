from akangatu.container import Container1


class Map(Container1):

    def _process_(self, data):
        if data.stream is None:
            print(f"{self.name} needs a Data object containing a stream.")
            print("Missing stream inside", data.id)
            exit()
        return data.update(self, stream=lambda: map(self.step.process, data.stream))
