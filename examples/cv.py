from kururu.tool.dataflow.file import File
from kururu.tool.enhancement.pca import PCA
from kururu.tool.evaluation.split import Split
from kururu.tool.learning.supervised.classification.svm import SVM

wk = File("iris.arff") * Split() * PCA    #* SVM

print(File("iris.arff").uuid.n)
print(File("iris.arff").uuid.print_matrix())
print(File("iris.arff").uuid.id)
print(SVM.id)

#
#
# data = wk.transform()
# print("iiiiiiiiiiiiiiiiii", data)
