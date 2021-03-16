import numpy as np
from sklearn.naive_bayes import GaussianNB

# samples
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
# labels
Y = np.array([1, 1, 1, 2, 2, 2])
# call the classifier
clf = GaussianNB()
# fit the samples and the labels to the classifier
clf.fit(X, Y)
# predict
print(clf.predict([[-0.8, -1]]))
