import json
from functools import cached_property
from random import choice

from pjdata.content.data import Data


class withSampling:
    """Transform data according to a sampleable configuration.

    Should be inherited together with a descendent of Transformer_
    (because name and config attributes are needed)"""
    trdata = Data()  # Data() is the identity Data and means "no trdata provided"

    def name(self):
        # noinspection PyUnresolvedReferences
        return super().name()

    @cached_property
    def config(self):
        # noinspection PyUnresolvedReferences
        return super().config

    def sample(self, track=False):  # TODO: seed
        config, choices = {}, {}
        for k, lst in self.parameters.items():  # TODO: nested dicts / key tracks from the root node
            idx = choice(range(len(lst)))
            config[k] = lst[idx]
            choices[k] = idx

        # noinspection PyArgumentList
        obj = self.__class__(**config) if not self.trdata else self.__class__(self.trdata, **config)

        return (obj, choices) if track else obj

    @cached_property
    def parameters(self):
        try:
            with open(f"resources/parameters/{self.name}.json", "r") as f:
                # return Parameters(self.name, self.context, json.load(f))
                params = json.load(f)
                for k, v in self.config.items():
                    params[k] = [v]
                return params
        except FileNotFoundError:
            raise Exception(f"Impossible to sample. Missing parameters file: {self.name}.json!")
