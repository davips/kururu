from abc import ABC

from cururu.mixin.operators import withOperators
from cururu.mixin.sampling import withSampling
from transf.datadependent import DataDependent_


class DataDependent(DataDependent_, withSampling, withOperators, ABC):
    """Operable and sampleable (training)data-dependent transformer"""
