from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import metrics
from sklearn import pipeline

# data to user
df = pd.DataFrame(
    columns=["x1", "x2", "y"], data=[[1, 16, 9], [4, 36, 2], [5, 5, 9], [3, 3, 15]]
)

train = df.iloc[:2]
test = df.iloc[2:]

train_x = train.drop('y', axis=1)
train_y = train["y"]

test_x = test.drop('y', axis=1)
test_y = test["y"]


@dataclass
class Aggeragator:

    client_tr: str = "../data/tr.csv"
    ...

    def aggregator(self):
        full_data = self.client_tr
        return full_data


class ExperimentalTransformer(BaseEstimator, TransformerMixin, Aggeragator):
    def __init__(self):
        print("call init")
        self.cst = 0.4

    def fit(self, X, y=None):
        """this will store all params you'll need to transform the data"""
        print("fit called")
        data = self.aggregator()
        print(data)
        self.cst = np.mean(X.x1)
        print(self.cst)
        return self

    def transform(self, X, y=None):
        print("transform called")
        X_ = X.copy()
        X_.x2 = self.cst * X_.x2
        return X_


# make pipeline
pipe2 = pipeline.Pipeline(
    steps=[
        ("experimental_trans", ExperimentalTransformer()),
        #("linear_model", linear_model.LinearRegression())
    ]
)

pipe2.fit(train_x, train_y)
train_x = pipe2.transform(train_x)
test_x = pipe2.transform(test_x)

print(train_x)
print(test_x)

# o fit é justamente para rodar o método de transformação e armazenar os parâmetros
# que podem ser utilizados no transform
# fit é aprendizago, transform é transformação

# um pipeline para o desafio de churn
# Aggregation => junta treino, teste, orders, products (base class to make this aggregation available)
# --- Each transformation that was needed will be abble to generate this data
# Outras transformações provavelmente não vão armazenar nd










