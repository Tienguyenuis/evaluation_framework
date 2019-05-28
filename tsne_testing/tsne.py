import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.decomposition import PCA, RandomizedPCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as mpl
from sklearn import preprocessing

import pylab

data = pd.read_csv("APP-BlogCatalog-edgelist.txt.embeddings-64.src")
y = pd.read_csv('BlogCatalog-labels.csv')
print(y)
print(data.head)
data.columns=['1']
X = data.loc[:,"1"]

for column in data.columns:
    if data[column].dtype == type(object):
        le = preprocessing.LabelEncoder()
        data[column] = le.fit_transform(data[column])

pca = PCA(0.95)
X_pca = pca.fit_transform(data)

tsne = TSNE()
X_tsne = tsne.fit_transform(X_pca[:10000])


mpl.rcParams['figure.figsize'] = (10.0, 10.0)
proj = pd.DataFrame(X_tsne)
proj.columns = ["comp_1", "comp_2"]
proj["labels"] = y
sns_plot = sns.lmplot("comp_1", "comp_2", hue = "labels", palette="Set1", data = proj.sample(5000) ,fit_reg=False)
sns_plot.savefig("app-blog64.png")



