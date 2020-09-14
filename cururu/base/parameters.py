class Parameters(dict):
    def __init__(self, name, path, parameters):
        super().__init__(parameters)
        self.name = name
        self.path = path
