from cururu.file import File
from cururu.svm import SVM

data = File("iris.arff").transform()
svm = SVM(data)
r = svm.transform(data)
print(r)
