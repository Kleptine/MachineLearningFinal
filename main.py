from sklearn import datasets, tree
import pylab as pl
from StringIO import StringIO
import sklearn


# Load in our data
iris = datasets.load_iris()

# Split between test/train/val
# trainSet, testSet = generateTrainTest(data)
trainSet = iris.data
testSet = iris.target

# Create various machine learning models
models = [ tree.DecisionTreeClassifier() ]

# Train all models
for model in models:
    model.fit(trainSet, testSet)
    
# Save the models

# Test models on various test sets with CV

# Output/Graph results
out = StringIO()
out = tree.export_graphviz(models[0], out_file=open("output", 'w'))

pl.scatter(iris.data[:, 0], iris.data[:, 1], marker='o')
pl.show()
