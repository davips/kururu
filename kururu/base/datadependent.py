from abc import ABC

from kururu.mixin.operators import withOperators
from kururu.mixin.sampling import withSampling
from transf.datadependent import DataDependent_


class DataDependent(DataDependent_, withSampling, withOperators, ABC):
    """Operable and sampleable (training)data-dependent transformer"""
