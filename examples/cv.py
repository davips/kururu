from kururu.tool.dataflow.file import File
from kururu.tool.enhancement.pca import PCA
from kururu.tool.evaluation.metric import Metric
from kururu.tool.evaluation.split import Split
from kururu.tool.learning.supervised.classification.svm import SVM

wk = File("iris.arff") * Split() * PCA(n=2) * SVM * Metric(["accuracy", "history"])

data = wk.transform()
print("iiiiiiiiiiiiiiiiii\n", data.r)
