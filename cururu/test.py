from cururu.file import File
from cururu.svm import SVM
from pjdata.aux.uuid import UUID

data = File("iris.arff").transform()
svm = SVM()
data.trdata = data
r = svm.transform(data)
print("svm",svm.uuid)
print("svm*data", svm.uuid(data.uuid))
print("data*svm*data",data.uuid * svm.uuid(data.uuid))
print(r.uuid)

print(UUID(ignore_call=True)(UUID()))