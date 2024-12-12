import cudf
from glob import glob
from joblib import dump, load
import numpy as np
import pandas as pd
import random
from cuml.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, make_scorer, accuracy_score
from sklearn.model_selection import train_test_split, KFold, RandomizedSearchCV
import warnings

warnings.filterwarnings(
    "ignore", 
    message="To use pickling first train using float32 data to fit the estimator"
)

### X and y
def getXandY(Output_Vari):
    y_list = glob("/home/pj24001881/ku40001335/Greenness_NighttimeLight_WB/01_Data/*_y_" + Output_Vari + "*.csv")
    y = pd.read_csv(y_list[0], index_col=0)
    y = y.iloc[:,0].to_numpy()
    X_list = glob("/home/pj24001881/ku40001335/Greenness_NighttimeLight_WB/01_Data/*_X_" + Output_Vari + "*.csv")
    X = pd.read_csv(X_list[0], index_col=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, 
                                                        random_state=1)
    return X_train, X_test, y_train, y_test

Output_Vari = "Happinessoverall"
X_train, X_test, y_train, y_test = getXandY(Output_Vari)
X = pd.concat([X_train, X_test])
y = np.concatenate([y_train, y_test])
rf_reg =RandomForestRegressor(n_bins=256)
param_grid = {
    "n_estimators": list(range(1_000, 5_100, 200)),
    "max_depth": [8, 16, 24, 32],
    "max_features": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "min_samples_split": [2, 4, 8, 16, 32],
    "max_samples": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
}
class RandomRunNFoldsKFold(KFold):
    def __init__(self, n_splits=10, random_state=None, run_splits=3, **kwargs):
        super().__init__(n_splits=n_splits, shuffle=True, random_state=random_state, **kwargs)
        self.random_state = random_state
        self.actual_splits = run_splits  # Number of actual splits to use

    def split(self, X, y=None, groups=None):
        folds = list(super().split(X, y, groups))
        if self.random_state is not None:
            random.seed(self.random_state)
        selected_folds = random.sample(folds, self.actual_splits)
        for train_index, test_index in selected_folds:
            yield train_index, test_index

    def get_n_splits(self, X=None, y=None, groups=None):
        return self.actual_splits

rkfcv = RandomRunNFoldsKFold(n_splits=10, run_splits=3, random_state=42)
random_search = RandomizedSearchCV(
    estimator=rf_reg,
    param_distributions=param_grid,
    n_iter=1_000,  # Number of parameter settings to sample
    scoring="r2",
    cv=rkfcv,  # 3-fold cross-validation
    random_state=42,
    verbose=2,
    return_train_score = True
)

# Fit the model
random_search.fit(X, y)
CV_result = random_search.cv_results_
pd.DataFrame(CV_result).sort_values(by='rank_test_score', ascending=True).loc[:,:].head()
dump(random_search, '/home/pj24001881/ku40001335/Greenness_NighttimeLight_WB/03_Results/RandomSearch1000_5hyper_v2.joblib')
pd.DataFrame(CV_result).sort_values(by='rank_test_score', ascending=True).to_csv('/home/pj24001881/ku40001335/Greenness_NighttimeLight_WB/03_Results/RandomSearch1000_hyper_v2.csv')

