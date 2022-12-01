from sklearn import svm
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn import tree
import pandas as pd
import numpy as np

exel = pd.read_excel('TOP500_202211.xlsx', index_col=None, header=0)
df = exel.iloc[:, [0, 9, 13, 18]]
df = df.dropna()
df = df.reset_index(drop=True)

X = df.iloc[:, [2, 3]]
Y = df.iloc[:, 1]
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y, random_state=0)

svc = svm.SVC(kernel='rbf', C=1).fit(X_train, y_train)
Z = svc.predict(X_test)

plt.scatter(X_test.iloc[Z < 2018, 1], X_test.iloc[Z < 2018, 0], c='black', marker='o', s=50, label="older")
plt.scatter(X_test.iloc[Z == 2018, 1], X_test.iloc[Z == 2018, 0], c='orange', marker='o', s=50, label="2018")
plt.scatter(X_test.iloc[Z == 2019, 1], X_test.iloc[Z == 2019, 0], c='blue', marker='o', s=50, label="2019")
plt.scatter(X_test.iloc[Z == 2020, 1], X_test.iloc[Z == 2020, 0], c='green', marker='o', s=50, label="2020")
plt.scatter(X_test.iloc[Z == 2021, 1], X_test.iloc[Z == 2021, 0], c='yellow', marker='o', s=50, label="2021")
plt.scatter(X_test.iloc[Z == 2022, 1], X_test.iloc[Z == 2022, 0], c='red', marker='o', s=50, label="2022")

plt.grid()
plt.legend()
plt.xlabel('Power in kW')
plt.ylabel('Rmax [TFlop/s]')
plt.show()

print("Accuracy on SVC model: ", svc.score(X_test, y_test))

dec_tree = tree.DecisionTreeClassifier().fit(X_train, y_train)
print(f"Score for train test in tree model: {dec_tree.score(X_train, y_train)}")
print(f"Score for test set in tree model: {dec_tree.score(X_test, y_test)}")

class_name = np.unique(list(map(str, df['Year'].tolist())))
feature = [str(i) for i in X.columns]
plt.figure()
tree.plot_tree(dec_tree, feature_names=feature, class_names=class_name, filled=True)
plt.title("Decision tree")
plt.show()
