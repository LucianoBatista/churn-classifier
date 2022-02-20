import pandas as pd

from src.feat_engineering import transformers
from sklearn import pipeline, ensemble, metrics, preprocessing


def run_pipeline():
    # getting the data paths
    data = transformers.DataAggregator()

    # loading training and testing data
    client_tr = pd.read_csv(data.client_tr_path, parse_dates=["birthdate"])
    client_ts = pd.read_csv(data.client_ts_path, parse_dates=["birthdate"])

    # putting on scikit conventions
    y_tr = client_tr[["is_churn"]]
    y_ts = client_ts[["is_churn"]]
    X_tr = client_tr.drop(["is_churn"], axis=1)
    X_ts = client_ts.drop(["is_churn"], axis=1)

    # model
    rfc_basic = ensemble.RandomForestClassifier(n_estimators=500, verbose=4)

    # our pipeline
    pipe1 = pipeline.Pipeline(
        steps=[
            ("extract_features", transformers.FeatureExtraction()),
            ("random_forest_baseline", rfc_basic),
        ]
    )

    pipe1.fit(X_tr, y_tr)
    y_pred = pipe1.predict(X_ts)
    print(metrics.roc_auc_score(y_ts, y_pred))
    # X_tr_transformed = pipe1.transform(X_tr)
    # pipe1.transform(X_ts)


if __name__ == "__main__":
    run_pipeline()
