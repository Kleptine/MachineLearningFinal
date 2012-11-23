from sklearn import datasets, tree
import matplotlib.pyplot as plt
import numpy as np
from StringIO import StringIO
import sklearn


# Load in our data
iris = datasets.load_iris()

# Split between test/train/val
# trainSet, testSet = generateTrainTest(data)
trainX = iris.data
trainY = iris.target

# Create various machine learning models
models = [ tree.DecisionTreeClassifier() ]

# Train all models
for model in models:
    model.fit(trainX, trainY)
    
# Save the models

# Test models on various test sets with CV

# Output/Graph results
#pl.scatter(iris.data[:, 0], iris.data[:, 1], marker='o')
#pl.show()

x = np.linspace(0, 6*np.pi, 100)
y = np.sin(x)

# Turn on interactive mode
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

for phase in np.linspace(0, 10*np.pi, 500):
    line1.set_ydata(np.sin(x + phase))
    fig.canvas.draw()