# FYS-STK4155 - H2020 - UiO
# Project 1
# Author: Fabio Rodrigues Pereira
# E-mail: fabior@uio.no


import numpy as np
from scipy import stats
from sklearn.linear_model import Lasso


class OLS:

    def __init__(self, random_state=None):

        if random_state is not None:
            np.random.seed(random_state)

        self.random_state = random_state

        self.coef_ = None
        self.coef_var = None
        self.z_var = None

    def fit(self, X, z):
        self.coef_ = np.linalg.pinv(X.T @ X) @ X.T @ z
        self.coef_var = np.linalg.pinv(X.T @ X)
        self.z_var = np.var(z)

    def predict(self, X):
        """Predicts the response variable from the design
        matrix times the optimal beta.

        :param X: np.array: Given explanatory variables.

        :return: np.array: Predictions z given X.
        """
        return X @ self.coef_

    def coef_confidence_interval(self, percentile=0.95):
        """ Calculates the confidence interval of the coefficients.

        :param percentile: float: Significance level

        :return: array: Beta Confidence intervals.
        """
        cov = self.z_var * self.coef_var
        std_err_coef = np.sqrt(np.diag(cov))
        z_score = stats.norm(0, 1).ppf(percentile)

        return z_score * std_err_coef


class Ridge(OLS):

    def __init__(self, lambda_=1, random_state=None):
        super().__init__(random_state)
        self.lambda_ = lambda_

    def fit(self, X, z):
        p = np.shape(X)[1]
        I = np.identity(p) * self.lambda_
        self.coef_ = np.linalg.pinv((X.T @ X) + I) @ X.T @ z

    def set_lambda(self, new_lambda):
        self.lambda_ = new_lambda


class LassoModel(Lasso):

    def __init__(self, alpha=1, fit_intercept=False, random_state=None):
        super().__init__(alpha, fit_intercept, random_state)

    def set_lambda(self, new_lambda):
        self.alpha = new_lambda