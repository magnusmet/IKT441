import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split

import warnings
warnings.simplefilter("ignore")

data = [[float(i) for i in i.split()] for i in open("yeast.data").readlines() if i.strip()]
training = [[float(i) for i in i.split()] for i in open("yeast_tr.data").readlines() if i.strip()]
testing = [[float(i) for i in i.split()] for i in open("yeast_tst.data").readlines() if i.strip()]

y_training = []
y_testing = []
y_data = []

for i in training:
        y_training.append(i[-1])
        del i[-1]

for i in testing:
        y_testing.append(i[-1])
        del i[-1]

train, test = train_test_split(data,test_size=0.1)

y_train = []
y_test = []


for i in train:
        y_train.append(i[-1])
        del i[-1]

for i in test:
        y_test.append(i[-1])
        del i[-1]





X = np.array(training)
Y = np.array(y_training)
X_ = np.array(testing)
Y_ = np.array(y_testing)
X2 = np.array(train)
Y2 = np.array(y_train)
X_2 = np.array(test)
Y_2 = np.array(y_test)


C=1.0
gamma = 0.5
svm_linear = svm.SVC(kernel='linear',C=C,gamma=gamma).fit(X2,Y2)
svm_polynomial = svm.SVC(kernel='poly',C=C,gamma=gamma).fit(X2,Y2)
svm_rbf = svm.SVC(kernel='rbf',C=C,gamma=gamma).fit(X2,Y2)
svm_sigmoid = svm.SVC(kernel='sigmoid',C=C,gamma=gamma).fit(X2,Y2)

for i in range(100):
    print("Testing round: "),i
    print("Linear")
    print(svm_linear.score(X_2,Y_2))
    print("Poly")
    print(svm_polynomial.score(X_2,Y_2))
    print("RBF")
    print(svm_rbf.score(X_2,Y_2))
    print("Sigmoid")
    print(svm_sigmoid.score(X_2,Y_2))


# def testSVM(svm):
#     numcorrect = 0
#     numwrong = 0
#     for correct,testing in ((0,zero),(1,one)):
#         for d in testing:
#             r = svm.predict(d)[0]
#             if(r==correct):
#                 numcorrect += 1
#             else:
#                 numwrong += 1
#     print "Correct",numcorrect
#     print "Wrong",numwrong




