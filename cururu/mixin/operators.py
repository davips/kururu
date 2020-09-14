from cururu.operator.binary.chain import Chain
from cururu.operator.binary.stream import Stream
from transf.mixin.operand import asOperand


class withOperators(asOperand):
    def available_operators(self):
        return [Chain, Stream]
