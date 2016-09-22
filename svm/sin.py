# simple prediction, source: http://stackoverflow.com/questions/24517858/time-series-forecasting-with-support-vector-regression

import numpy as np
from matplotlib import pyplot as plt
from sklearn.svm import SVR

X = np.arange(0,100)
Y = np.sin(X)

print X
print Y

a = 0
b = 10
x = []
y = []
while b <= 100:
    x.append(Y[a:b])
    a += 1
    b += 1
b = 10

print x

while b <= 90:
    y.append(Y[b])
    b += 1

print y

svr_rbf = SVR(kernel='rbf', C=1, gamma=0.1)
y_rbf = svr_rbf.fit(x[:81], y).predict(x)

figure = plt.figure()
tick_plot = figure.add_subplot(1, 1, 1)
tick_plot.plot(X, Y, label='data', color='green', linestyle='-')
tick_plot.axvline(x=X[-10], alpha=0.2, color='gray')
tick_plot.plot(X[10:], y_rbf[:-1], label='data', color='blue', linestyle='--')
plt.show()