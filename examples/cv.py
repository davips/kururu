from kururu.tool.dataflow.file import File
from kururu.tool.enhancement.binarize import Binarize
from kururu.tool.enhancement.pca import PCA
from kururu.tool.evaluation.metric import Metric2
from kururu.tool.evaluation.split import Split
from kururu.tool.learning.supervised.classification.svm import SVM2

wk = File("abalone3.arff") * Binarize * Split * PCA(n=3) * SVM2 * Metric2(["accuracy", "history"])
# TODO: put markers in history delimiting macros
# TODO: File e futuros como esses markers podem ter o mesmo uuid p/ diferentes configs
#  (pois terão algum rótulo único, embora uuuid identidade);
#   um problema é no tatu, precisaria referenciar cada item no historico por item.uuid * data.uuid e não mais apenas por item.uuid.
#   mas perde o benefício de economizar espaço das entradas repetidas.
#  Na verdade, quem tem uuid identidade, não é armazenável e requer um hash no texto, prefixado com IDENT
data = wk.transform()
print("train:\n", data.inner.r, list(data.inner.history.clean))
print("test:\n", data.r, list(data.history.clean))
