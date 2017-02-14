import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split

import warnings
warnings.simplefilter("ignore")

data = [[float(i) for i in i.split()] for i in open("yeast.data").readlines() if i.strip()]

train, test = train_test_split(data,test_size=0.1)

y_train = []
y_test = []

for i in train:
        y_train.append(i[-1])
        del i[-1]

for i in test:
        y_test.append(i[-1])
        del i[-1]

X = np.array(train)
Y = np.array(y_train)
X_ = np.array(test)
Y_ = np.array(y_test)

C=1.0
gamma = 0.5
svm_linear = svm.SVC(kernel='linear',C=C,gamma=gamma).fit(X, Y)
svm_polynomial = svm.SVC(kernel='poly',C=C,gamma=gamma).fit(X, Y)
svm_rbf = svm.SVC(kernel='rbf',C=C,gamma=gamma).fit(X, Y)
svm_sigmoid = svm.SVC(kernel='sigmoid',C=C,gamma=gamma).fit(X, Y)

avgLin = 0.0
avgPol = 0.0
avgRbf = 0.0
avgSig = 0.0

run = 1000

for i in range(run):
    print("Testing round: "),i
    print("Linear")
    print(svm_linear.score(X_, Y_))
    avgLin += svm_linear.score(X_, Y_)
    print("Poly")
    print(svm_polynomial.score(X_, Y_))
    avgPol += svm_polynomial.score(X_, Y_)
    print("RBF")
    print(svm_rbf.score(X_, Y_))
    avgRbf += svm_rbf.score(X_, Y_)
    print("Sigmoid")
    print(svm_sigmoid.score(X_, Y_))
    avgSig += svm_sigmoid.score(X_, Y_)

print("Average Linear Performance:", (avgLin/run))
print("Average Poly Performance:", (avgPol/run))
print("Average RBF Performance:", (avgRbf/run))
print("Average Sigmoid Performance: ", (avgSig/run))








