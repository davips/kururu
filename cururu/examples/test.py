from cururu.tool.dataflow.file import File
from cururu.tool.evaluation.partition import Partition
from cururu.tool.enhancement.pca import PCA
from cururu.tool.evaluation.split import Split
from cururu.tool.learning.supervised.classification.svm import SVM
from pjdata.aux.uuid import UUID

data = File("iris.arff").transform()

print("SVM()(trdata)")
svm = SVM()
r = svm(data).transform(data)
print(r.uuid.__str__() + "\n")

print("SVM(trdata)")
svm = SVM(data)
r = svm.transform(data)
print(r.uuid.__str__() + "\n")

print("SVM() + data.trdata")
svm = SVM()
data.trdata = data
r = svm.transform(data)
print(r.uuid.__str__() + "\n")

print("svm\t\t", svm.uuid)
print("svm*data\t", svm.uuid(data.uuid))
print("data*svm*data", data.uuid * svm.uuid(data.uuid))
print(r.uuid)

print()
print("---------------------------")
print()

print("PCA()(trdata)")
data.trdata = None
pca = PCA()
r = pca(data).transform(data)
print(r.uuid.__str__() + "\n")

print("PCA(trdata)")
pca = PCA(data)
r = pca.transform(data)
print(r.uuid.__str__() + "\n")

print("PCA() + data.trdata")
pca = PCA()
data.trdata = data
r = pca.transform(data)
print(r.uuid.__str__() + "\n")

print("PCA\t\t", pca.uuid)
print("PCA*data\t", pca.uuid(data.uuid))
print("data*PCA*data", data.uuid * pca.uuid(data.uuid))
print(r.uuid)

print()
print("---------------------------")
print()
#
# print("Split()")
# data.trdata = None
# split = Split()
# r = split.transform(data)
# print(r.uuid.__str__() + "\n")
#
# print("Split() + data.trdata")
# split = Split()
# data.trdata = data
# r = split.transform(data)
# print(r.uuid.__str__() + "\n")
#
# print("Split\t\t", split.uuid)
# print("Split*data\t", split.uuid(data.uuid))
# print("data*Split*data", data.uuid * split.uuid(data.uuid))
# print(r.uuid)

print()
print("---------------------------")
print()

# print("Partition()")
# data.trdata = None
# partition = Partition()
# r = partition.transform(data)
# print(r.uuid.__str__() + "\n")
#
# print("Partition() + data.trdata")
# partition = Partition()
# data.trdata = data
# r = partition.transform(data)
# print(r.uuid.__str__() + "\n")
#
# print("Partition\t\t", partition.uuid)
# print("Partition*data\t", partition.uuid(data.uuid))
# print("data*Partition*data", data.uuid * partition.uuid(data.uuid))
# print(r.uuid)

r = PCA * SVM
print(r)
