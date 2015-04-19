
import pickle
import os
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin

cur_dir = os.path.dirname(__file__)
data_path = os.path.join(cur_dir, '../data')
obs_path = os.path.join(data_path, 'obs.p')

class FitlessMixin(BaseEstimator, TransformerMixin):
    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self


class Dicter(FitlessMixin):
    def transform(self, str_sets):
        return [{k: 1 for k in str_set} for str_set in str_sets]

    def inverse_transform(self, dict_list):
        return [set(d.keys()) for d in dict_list]

feat_pipe = make_pipeline(
    Dicter(),
    DictVectorizer()
)


def featurize(obs, save=False):
    X_raw, y_raw = zip(*obs)

    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    x_names, x_types = zip(*X_raw)
    # todo: combo names and types
    x = feat_pipe.fit_transform(x_names)

    if save:
        pickle.dump(le, open(os.path.join(data_path, 'le.p'), 'wb'))
        pickle.dump(feat_pipe, open(os.path.join(data_path, 'feat_pipe.p'), 'wb'))

    return x, y


if __name__ == '__main__':
    obs = pickle.load(open(obs_path, 'rb'))
    x, y = featurize(obs, save=True)


