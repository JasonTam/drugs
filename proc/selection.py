import os
from proc.featurize import featurize
import pickle
from sklearn.base import TransformerMixin
from sklearn.pipeline import make_pipeline

cur_dir = os.path.dirname(__file__)
data_path = os.path.join(cur_dir, '../data')
obs_path = os.path.join(data_path, 'obs.p')


class DenseTransformer(TransformerMixin):

    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self


if __name__ == '__main__':
    obs = pickle.load(open(obs_path, 'rb'))
    x, y = featurize(obs, save=False)

    ap = AprioriAlg()   # todo: write this

    clf = make_pipeline(
        DenseTransformer(),
        ap,
    )

    clf.fit(x, y)

