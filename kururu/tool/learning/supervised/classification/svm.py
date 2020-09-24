from sklearn.svm import NuSVC

from aiuna.config import globalcache
from aiuna.content.data import Data
from akangatu.datadependent import DataDependent
from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.dataflow.delin import DelIn


class SVM(DataDependent):
    """  """

    def __init__(self, *args, **kwargs):  # TODO :params and defaults
        self._config = kwargs

    def _transform_(self, data: Data):
        z = self.model(data.inner).predict(data.X)
        return data.replace(self, z=z)

    def _config_(self):
        return self._config

    @globalcache
    def model(self, data):
        nusvc = NuSVC(**self.config)
        nusvc.fit(*data.Xy)
        return nusvc


class SVM2(asMacro, SVM):
    def _transformer_(self):
        return SVM(**self.held) * In(AutoIns * SVM(**self.held) * DelIn)

    # x = 0.00001
    # l = []
    # for i in range(128):
    #     x = x * 1.1
    #     l.append(x)
    # print(l)

    """
default = SVM(tr).transform(ts)
default = SVM(tr).transform([tr, ts])
default = SVM(tr).transform([ts1, ts2, ts3])
simples = SVM(tr, ...).transform(d)
workf = File("iris") * Bin * Split(...) * dual(PCA(n=5) * dual(SVM(...))
expr = File("iris") * Split(...) * PCA(tr) * SVM(tr)

                                -> ts{tr}
expr = File("iris") * Split(...) * dual(NR(), Id()) * dual(PCA()) * dual(Id(), SVM())
Split(...) * PCA() * SVM()
= Chain(Split(...), dual(PCA())) * SVM()
= Chain(Split(...), dual(PCA()), dual(SVM()))

expr.transform(ts)
expr.sample(ts).transform(ts)
    
SVM(tr).transform(ts)       ->  default
SVM(tr, ...).transform(ts)  ->  configured

SVM(tr).sample()            ->  random
SVM(tr, ...).sample()       ->  partially configured/random
  
SVM()(tr).transform(ts)     ->  default
SVM().sample()              ->  SVM(...)
SVM().sample()(tr)          ->  random
SVM(...)                    ->  lambda  
SVM(...)(tr).transform(tr)  ->  configured
SVM(...)(tr).sample(ts)     ->  partially configured/random

Todo transformer transforma o data passado (externo).
Alguns dependem do data interno (trdata) como dado de entrada.
Para alterar dado interno, há dois modificadores: Inner e Both
Inner(NR()) -> aplica no trdata [mas transforma ambos! histórico: InnerNR muda o de fora e NR o de dentro]
Both(PCA()) -> aplica em ambos, mas treina sempre no interno [histórico: BothPCA muda externo e PCA muda interno] 
    """
