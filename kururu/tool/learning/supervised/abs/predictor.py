from abc import ABC, abstractmethod

from transf.config import globalcache
from aiuna.content.data import Data
from akangatu.ddstep import DDStep


class Predictor(DDStep, ABC):
    """  """

    def _process_(self, data: Data):
        dic = {"Z": lambda: self.model(data.inner).predict(data.X)}
        if "probability" in self.config and self.config["probability"]:
            dic["P"] = lambda: self.model(data.inner).predict_proba(data.X)
        return data.update(self, **dic)

    @globalcache
    def model(self, data):
        return self._model_(data)

    @abstractmethod
    def _model_(self, data):
        pass

    # x = 0.00001
    # l = []
    # for i in range(128):
    #     x = x * 1.1
    #     l.append(x)
    # print(l)

    """
default = SVM(tr).process(ts)
default = SVM(tr).process([tr, ts])
default = SVM(tr).process([ts1, ts2, ts3])
simples = SVM(tr, ...).process(d)
workf = File("iris") * Bin * Split(...) * dual(PCA(n=5) * dual(SVM(...))
expr = File("iris") * Split(...) * PCA(tr) * SVM(tr)

                                -> ts{tr}
expr = File("iris") * Split(...) * dual(NR(), Id()) * dual(PCA()) * dual(Id(), SVM())
Split(...) * PCA() * SVM()
= Chain(Split(...), dual(PCA())) * SVM()
= Chain(Split(...), dual(PCA()), dual(SVM()))

expr.process(ts)
expr.sample(ts).process(ts)
    
SVM(tr).process(ts)       ->  default
SVM(tr, ...).process(ts)  ->  configured

SVM(tr).sample()            ->  random
SVM(tr, ...).sample()       ->  partially configured/random
  
SVM()(tr).process(ts)     ->  default
SVM().sample()              ->  SVM(...)
SVM().sample()(tr)          ->  random
SVM(...)                    ->  lambda  
SVM(...)(tr).process(tr)  ->  configured
SVM(...)(tr).sample(ts)     ->  partially configured/random

Todo step transforma o data passado (externo).
Alguns dependem do data interno (trdata) como dado de entrada.
Para alterar dado interno, há dois modificadores: Inner e Both
Inner(NR()) -> aplica no trdata [mas transforma ambos! histórico: InnerNR muda o de fora e NR o de dentro]
Both(PCA()) -> aplica em ambos, mas treina sempre no interno [histórico: BothPCA muda externo e PCA muda interno] 
    """
