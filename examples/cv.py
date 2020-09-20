from kururu.tool.dataflow.file import File
from kururu.tool.enhancement.binarize import Binarize
from kururu.tool.enhancement.pca import PCA
from kururu.tool.evaluation.metric import Metric2
from kururu.tool.evaluation.split import Split
from kururu.tool.learning.supervised.classification.svm import SVM2

wk = File("abalone3.arff") * Binarize * Split * PCA(n=3) * SVM2 * Metric2(["accuracy", "history"])

data = wk.transform()
print("train:\n", data.inner.r, list(data.inner.history.clean))
print("test:\n", data.r, list(data.history.clean))
