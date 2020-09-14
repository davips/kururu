from abc import ABC

from cururu.mixin.operators import withOperators
from cururu.mixin.sampling import withSampling
from transf.dataindependent import DataIndependent_


class DataIndependent(DataIndependent_, withSampling, withOperators, ABC):
    """Operable and sampleable data transformer that doesn't dependent on (training) data."""
