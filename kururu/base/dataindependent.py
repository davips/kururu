from abc import ABC

from kururu.mixin.operators import withOperators
from kururu.mixin.sampling import withSampling
from transf.dataindependent import DataIndependent_


class DataIndependent(DataIndependent_, withSampling, withOperators, ABC):
    """Operable and sampleable data transformer that doesn't dependent on (training) data."""
