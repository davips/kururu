from functools import cached_property

from transf.transformer import Transformer


class Chain(Transformer):
    def __init__(self, transformers, **kwargs):
        self.transformers = transformers
        self._config = {"transformers": transformers}

    def _transform_(self, data):
        pass

    def _config_(self):
        return self._config

    def sample(self, track=False):  # TODO: seed
        return Chain(transf.sample(track) for transf in self.transformers)

    @cached_property
    def parameters(self):  # override
        # return Parameters(self.name, self.context, {"transformers": [transf.parameters for transf in self.transformers]})
        return {"transformers": [transf.parameters for transf in self.transformers]}


def traverse(params):
    """Assume all containers are configless"""
    # TODO: terminar essa tentativa de percorrer e talvez casar com tracking de valores previos
    for k, v in params.items():
        if k == "transformers":
            for transf in v:
                traverse(transf.parameters)
        else:
            pass
