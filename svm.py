import numpy as np


X= np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
Y=np.array([-1,0,1])
test=np.array([[1,2,3,4],[1,6,7,8],[1,10,11,12]])

from sklearn import svm
svmkernel = svm.SVC(kernel='rbf')
clf = svm.SVC(gamma=0.001, C=100.)
svc = svm.SVC(kernel='linear')
print clf.fit(X,Y)
print clf.predict(test)
