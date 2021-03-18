from sklearn import tree
X = [[0, 0], [1, 1]]
Y = [0, 1]
clf = tree.DecisionTreeClassifier(min_samples_split=2)
clf = tree.DecisionTreeClassifier(min_samples_split=50)
clf = clf.fit(X, Y)
print(clf.predict([[2., 2.]]))