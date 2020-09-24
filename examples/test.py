from aiuna import config
from aiuna.file import File
from cruipto.uuid import UUID
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.enhancement.pca import PCA1, PCA
from kururu.tool.evaluation.metric import Metric, Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.split import Split, Split1
from kururu.tool.learning.supervised.classification.svm import SVM, SVM2
from kururu.tool.manipulation.slice import Slice
from transf._ins import Ins

data = File("iris.arff").transform()
print("iris", data.id)
print("iden", UUID.identity)

print("default p/ treinar depois com data externo:  SVM()(inner)")
svm = SVM()
r = svm(data).transform(data)
print("svm\t\t", svm.id)
print("svm(data)\t", svm(data).id)
print("inner*svm\t", Ins(data).uuid * svm.uuid)
print("data*inner*svm", data.uuid * Ins(data).uuid * svm.uuid)
print(r.id + "\n")

print("default treinado:  SVM(inner)")
model = SVM(data)
r = model.transform(data)
print("svm\t\t", svm.id)
print("model\t", model.id)
print("inner\t", Ins(data).uuid )
print("inner*svm\t", Ins(data).uuid * SVM().uuid)
print("data*inner*svm", data.uuid * Ins(data).uuid * SVM().uuid)
print(r.id + "\n")

print("default p/ treinar depois com data interno:  SVM() + data.inner")
print("svm\t\t", svm.uuid)
data2 = AutoIns().transform(data)
data = data2
print("data com inner\t", data.id)
print("data*svm", data.uuid * svm.uuid)
svm = SVM2()

r = svm.transform(data)
config.SHORT_HISTORY=not False
print(r.id + "\n", r.history)
print("***********************************************")

print()
print("---------------------------")
print()
data = File("iris.arff").transform()

print("PCA()(inner)")
data.inner = None
pca = PCA1()
r = pca(data).transform(data)
print(r.uuid.__str__() + "\n")

print("PCA(inner)")
pca = PCA1(data)
r = pca.transform(data)
print(r.uuid.__str__() + "\n")

print("PCA() + data.inner")
pca = PCA1()
data.inner = data
r = pca.transform(data)
print(r.uuid.__str__() + "\n")
data.inner = None

print("PCA\t\t", pca.uuid)
print("PCA*data\t", pca.uuid(data.uuid))
print("data*PCA*data", data.uuid * pca.uuid(data.uuid))
print(r.uuid)

print()
print("---------------------------")
print()

print("Split()")
data.inner = None
split = Split()
r = split.transform(data)
print(r.uuid.__str__() + "\n")

print("Split() + data.inner")
split = Split()
r = split.transform(data)
print(r.uuid.__str__() + "\n")

print("Split\t\t", split.uuid)
print("Split*data\t", split.uuid(data.uuid))
print("data*Split*data", data.uuid * split.uuid(data.uuid))
print(r.uuid)

print()
print("---------------------------")
print()

print("Partition()")
data.inner = None
partition = Partition()
r = partition.transform(data)
print(r.uuid.__str__() + "\n")

print("Partition() + data.inner")
partition = Partition()
data.inner = data
r = partition.transform(data)
print(r.uuid.__str__() + "\n")

print("Partition\t\t", partition.uuid)
print("Partition*data\t", partition.uuid(data.uuid))
print("data*Partition*data", data.uuid * partition.uuid(data.uuid))
print(r.uuid)

r = PCA1 * SVM
print(type(r), r)

data.inner = None
d = (SVM(data) * Slice()).transform(data)
print(d.X)
print(d.history)

print(PCA1.sample())

import numpy as np

np.random.seed(2)
p = PCA1(data).sample()
print(p, data.X.shape[1])
d = p.transform(data)
tr = d.inner
print(data.id, "inner                    ", tr and tr.id, "!!!!!!!!!!!!!", d.failure, "        ", d.id)
# print((PCA * SVM).sample().transform(data))
