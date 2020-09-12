from functools import lru_cache

from transf.datadependent import DataDependent
from sklearn.svm import NuSVC


class SVM(DataDependent):
    """  """

    def __init__(self, trdata=None, **kwargs):
        self._trdata = trdata
        self._config = kwargs

    def _deptransform_(self, data, trdata):
        z = self.model(trdata).predict(data.X)
        return data.replace(self, truuid=trdata.uuid, z=z)

    def _config_(self):
        return self._config

    def _trdata_(self):
        return self._trdata

    @lru_cache()
    def model(self, data):
        nusvc = NuSVC(**self.config)
        nusvc.fit(*data.Xy)
        return nusvc

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

SVM()                       ->  lambda  
SVM()(tr).transform(ts)     ->  default
SVM().sample()              ->  SVM(...)
SVM().sample()(tr)          ->  random
SVM(...)                    ->  lambda  
SVM(...)(tr).transform(tr)  ->  configured
SVM(...)(tr).sample(ts)     ->  partially configured/random

    """
