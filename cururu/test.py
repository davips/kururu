from pjdata.creation import read_arff
from transf.svm import SVM

data = read_arff("iris.arff")[1]
svm = SVM(data)
r = svm.transform(data)
print((list(r.history.clean)[0]))
