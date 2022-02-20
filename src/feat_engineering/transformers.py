import datetime
from pathlib import Path
from src.feat_engineering import composer

import numpy as np
import matplotlib.pyplot as plt
from IPython.core.display_functions import display
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pandas as pd
from dataclasses import dataclass


@dataclass
class DataAggregator:

    product_path_db: str = Path("../../data/product.csv")
    orders_path_db: str = Path("../../data/orders.csv")
    client_tr_path: str = Path("../../data/client.train.csv")
    client_ts_path: str = Path("../../data/client.test.csv")
    order_w_clients_w_products: pd.DataFrame = pd.DataFrame()

    def get_full_data(self) -> pd.DataFrame:
        product_db = pd.read_csv(self.product_path_db)
        orders_db = pd.read_csv(self.orders_path_db, parse_dates=["datetime"])
        client_tr = pd.read_csv(self.client_tr_path, parse_dates=["birthdate"])
        client_ts = pd.read_csv(self.client_ts_path, parse_dates=["birthdate"])

        # concat clients and guarantee
        concat_pd = pd.concat([client_tr, client_ts], axis=0).drop_duplicates(
            ["client_id"]
        )

        # merging orders and products
        orders_w_clients = orders_db.merge(right=concat_pd, on="client_id", how="left")

        self.order_w_clients_w_products = orders_w_clients.merge(
            right=product_db, on="product_id", how="left"
        )
        return self.order_w_clients_w_products


class FeatureExtraction(BaseEstimator, TransformerMixin, DataAggregator):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        print("Nothing to fit yet")
        return self

    def transform(self, X, y=None):
        composition = composer.compose(
            self._make_age,
            self._encoding_gender,
            self._add_count_payment_method,
            self._add_count_device_feat,
            self._add_count_unit_ordered,
            self._add_count_source_method,
            self._cleanup_unsued_features
        )
        _X = composition(X)
        return _X

    def _make_age(self, X: pd.DataFrame) -> pd.DataFrame:
        print("Creating age column!")
        _X = X.copy()
        _X["age"] = datetime.date.today().year - _X["birthdate"].dt.year
        return _X

    def _encoding_gender(self, X: pd.DataFrame) -> pd.DataFrame:
        print("Enconding gender!")
        _X = X.copy()
        # numeric labels to gender
        to_replace = {"gender": {"cg2": 0, "cg1": 1}}
        _X.replace(to_replace, inplace=True)
        return _X

    def _add_count_payment_method(self, X: pd.DataFrame) -> pd.DataFrame:
        print("Adding a payment method columns by client!")
        _X = X.copy()
        full_data = self.get_full_data()

        payment_methods_categories = []
        for i in range(1, 15):
            if i < 10:
                suffix = f"0{str(i)}"
            else:
                suffix = str(i)
            pm = f"pm{suffix}"
            payment_methods_categories.append(pm)

        # procedure to create a cross table counting pm by clients
        pm_type = pd.CategoricalDtype(categories=payment_methods_categories)
        full_data["payment_method"] = full_data["payment_method"].astype(pm_type)
        client_vs_pms = pd.crosstab(
            full_data["client_id"], full_data["payment_method"], dropna=False
        ).reset_index()

        df_to_return = _X.merge(right=client_vs_pms, on="client_id", how="left")

        return df_to_return

    def _add_count_device_feat(self, X: pd.DataFrame) -> pd.DataFrame:
        print("Adding a device method columns by client!")
        _X = X.copy()
        # full_data = DataAggregator().get_full_data()
        full_data = self.get_full_data()

        device_categories = []
        for i in range(1, 10):
            suffix = str(i)
            pm = f"dv{suffix}"
            device_categories.append(pm)

        # procedure to create a cross table counting pm by clients
        device_type = pd.CategoricalDtype(categories=device_categories)
        full_data["device"] = full_data["device"].astype(device_type)
        client_vs_pms = pd.crosstab(
            full_data["client_id"], full_data["device"], dropna=False
        ).reset_index()

        df_to_return = _X.merge(right=client_vs_pms, on="client_id", how="left")

        return df_to_return

    def _add_count_source_method(self, X: pd.DataFrame) -> pd.DataFrame:
        print("Adding a source method columns by client!")
        _X = X.copy()
        # full_data = DataAggregator().get_full_data()
        full_data = self.get_full_data()

        source_method = []
        for i in range(1, 15):
            if i < 10:
                suffix = f"0{str(i)}"
            else:
                suffix = str(i)
            sc = f"sc{suffix}"
            source_method.append(sc)

        # procedure to create a cross table counting pm by clients
        device_type = pd.CategoricalDtype(categories=source_method)
        full_data["source"] = full_data["source"].astype(device_type)
        client_vs_pms = pd.crosstab(
            full_data["client_id"], full_data["source"], dropna=False
        ).reset_index()

        df_to_return = _X.merge(right=client_vs_pms, on="client_id", how="left")

        return df_to_return

    def _add_count_unit_ordered(self, X: pd.DataFrame) -> pd.DataFrame:
        print("Adding a count on units ordered columns by client!")
        _X = X.copy()
        full_data = self.get_full_data()
        full_grouped_df = full_data.groupby(["client_id"])["units"].sum()

        df_to_return = _X.merge(right=full_grouped_df, on="client_id", how="left")

        return df_to_return

    def _add_mean_price_ordered(self):
        ...

    def _cleanup_unsued_features(self, X: pd.DataFrame) -> pd.DataFrame:
        return X.drop(["client_id", "birthdate", "state"], axis=1)