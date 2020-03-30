import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectPercentile, f_regression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.tree import DecisionTreeRegressor
from tpot.builtins import StackingEstimator

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: -665835346.7844422
exported_pipeline = make_pipeline(
    SelectPercentile(score_func=f_regression, percentile=17),
    StackingEstimator(estimator=DecisionTreeRegressor(ccp_alpha=0, criterion="mae", max_depth=10, max_features=8, min_samples_leaf=20, min_samples_split=13)),
    DecisionTreeRegressor(ccp_alpha=1, criterion="mse", max_depth=9, max_features=16, min_samples_leaf=1, min_samples_split=6)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)