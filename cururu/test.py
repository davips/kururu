from cururu.file import File
from cururu.pca import PCA
from cururu.svm import SVM
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
