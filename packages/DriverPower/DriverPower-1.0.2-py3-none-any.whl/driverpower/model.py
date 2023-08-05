""" Background mutation rate model

Two types of BMR model are supported:
1. Randomized lasso + GLM
2. Gradient boosting machine

"""

import logging
import sys
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LassoCV, RandomizedLasso
from sklearn.model_selection import KFold
from sklearn.utils import resample
from sklearn.metrics import r2_score, explained_variance_score
from scipy.special import logit
from driverpower.dataIO import read_feature, read_response, read_fi, read_param
from driverpower.dataIO import save_fi, save_prediction, save_model
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import xgboost as xgb
    import statsmodels.api as sm
    import statsmodels


logger = logging.getLogger('MODEL')


def run_bmr(model_name, X_path, y_path,
            fi_cut=0.5, fi_path=None,
            kfold=3, param_path=None,
            project_name='DriverPower', out_dir='./DriverPower.output/',
            save_pred=False):
    """ Wrapper function for BMR model.

    Args:
        model_name (str): 'GLM' or 'GBM'
        X_path (str): path to training X
        y_path (str): path to training y
        fi_cut (float): cutoff for feature importance
        fi_path (str): path to the feature importance
        kfold (int): K fold CV for GBM
        param_path (str): path to the GBM parameters pkl
        project_name (str): name of the project
        out_dir (str): directory for saving output files
        save_pred (bool): save the prediction for training set

    Returns:

    """
    use_features = read_fi(fi_path, fi_cut)
    run_feature_select = False if use_features else True
    X = read_feature(X_path, use_features)
    y = read_response(y_path)
    feature_names = X.columns.values
    # down-sampling 0 mutation elements
    pct_zero = y[y.nMut == 0].shape[0] / y.shape[0] * 100
    pct_req = 0.1
    if pct_zero > 99:  # This disable down-sampling
        logger.info('{:.2f}% elements have zero mutation. Downsampling to {}%'.format(pct_zero, pct_req*100))
        ct_req = int(y.shape[0] * pct_req)
        y_nonzero = y[y.nMut>0]
        y_zero = y[y.nMut==0]
        y_zero = y_zero.sample(n=ct_req, replace=False)
        y = pd.concat([y_nonzero, y_zero])
        del y_nonzero, y_zero
    # use bins with both X and y
    use_bins = np.intersect1d(X.index.values, y.loc[y.length>=100, :].index.values)
    logger.info('Use {} bins in model training'.format(use_bins.shape[0]))
    X = X.loc[use_bins, :].values  # X is np.array now
    y = y.loc[use_bins, :]
    if model_name in ('Binomial', 'NegativeBinomial'):
        # Scale data is necessary for GLM
        X, scaler = scale_data(X)
        if run_feature_select:
            # Run lasso to get alpha
            alpha = run_lasso(X, y)
            # Run rnd lasso to get feature importance
            fi_scores = run_rndlasso(X, y, alpha)
            fi = save_fi(fi_scores, feature_names, project_name, out_dir)
            # Remove unimportant features
            keep = (fi.importance >= fi_cut).values
            use_features = fi.name.values[keep]
            X = X[:, np.isin(feature_names, use_features)]
        # Run GLM to get trained model
        model = run_glm(X, y, model_name)
        yhat = (model.fittedvalues * y.length * y.N).values if model_name == 'Binomial' else model.fittedvalues
        # report metrics
        report_metrics(yhat, y.nMut.values)
        if save_pred:
            save_prediction(yhat, y, project_name, out_dir, model_name)
        # Run dispersion test
        pval, theta = dispersion_test(yhat, y.nMut.values) if model_name == 'Binomial' else (0, model.scale)
        # remove actual data from GLM model; save space
        with warnings.catch_warnings():
            # https://github.com/statsmodels/statsmodels/issues/3563
            warnings.filterwarnings('ignore', category=statsmodels.CacheWriteWarning)
            model.remove_data()
        # Save model info.
        model_info = {'model_name': model_name,
                      'model': model,
                      'scaler': scaler,
                      'pval_dispersion': pval,
                      'theta': theta,
                      'feature_names': feature_names,
                      'use_features': use_features,
                      'project_name': project_name}
    elif model_name == 'GBM':
        # calculate base margin
        offset = np.array(np.log(y.length+1/y.N) + np.log(y.N))
        # k-fold CV
        ks = KFold(n_splits=kfold)
        param = read_param(param_path)
        yhat = np.zeros(y.shape[0])
        k = 1  # idx of model fold
        fi_scores_all = pd.DataFrame(np.nan, columns=['fold' + str(i) for i in range(1, kfold+1)], index=feature_names)
        # model dict (key is the fold and value is the booster
        model = dict()
        X_dict = dict()  # dict to hold X for each fold (key)
        X_idx = dict()  # dict to hold index of X for each fold (key)
        # split data into k fold
        for valid, train in ks.split(range(X.shape[0])):
            logger.info('Split data fold {}/{}'.format(k, kfold))
            X_dict[k] = xgb.DMatrix(data=X[train, :], label=y.nMut.values[train], feature_names=feature_names)
            X_idx[k] = train
            # add offset
            X_dict[k].set_base_margin(offset[train])
            k += 1
        del X
        # train and predict
        for k in range(1, kfold+1):
            logger.info('Training GBM fold {}/{}'.format(k, kfold))
            # data fold used in validation
            k_valid = k + 1 if k < kfold else 1
            # train with fold k and valid with k_valid
            model[k] = run_gbm(X_dict[k], X_dict[k_valid], param)
            # predict on valid
            yhat[X_idx[k_valid]] = model[k].predict(X_dict[k_valid])
            # get feature importance score
            fi_scores_all['fold' + str(k)] = pd.Series(model[k].get_score(importance_type='gain'))
        # Save feature importance result
        fi_scores_all.fillna(0, inplace=True)
        fi_scores = fi_scores_all.mean(axis=1).values  # get average score for each feature
        save_fi(fi_scores, fi_scores_all.index.values, project_name, out_dir)
        # report metrics
        report_metrics(yhat, y.nMut.values)
        if save_pred:
            save_prediction(yhat, y, project_name, out_dir, model_name)
        # Run dispersion test
        pval, theta = dispersion_test(yhat, y.nMut.values)
        model_info = {'model_name': model_name,
                      'model': model,
                      'pval_dispersion': pval,
                      'theta': theta,
                      'kfold': kfold,
                      'params': param,
                      'feature_names': feature_names,
                      'project_name': project_name,
                      'model_dir': out_dir}
    else:
        logger.error('Unknown background model: {}. Please use Binomial, NegativeBinomial or GBM'.format(model_name))
        sys.exit(1)
    save_model(model_info, project_name, out_dir, model_name)
    logger.info('Job done!')


def scale_data(X, scaler=None):
    """ Scale X with robust scaling.
    
    Args:
        X (np.array): feature matrix indexed by binID.
        scaler (RobustScaler): pre-trained scaler. Default is None
        
    Returns:
        np.array: normalized feature matrix.
        RobustScaler: robust scaler fitted with training data,
            only returned when there is no pre-trained scaler.
    
    """
    if scaler is not None:
        return scaler.transform(X)
    else:
        scaler = RobustScaler(copy=False)
        scaler.fit(X)
        return scaler.transform(X), scaler


def run_lasso(X, y, max_iter=3000, cv=5, n_threads=1):
    """ Implement LassoCV in sklearn
    
    Args:
        X (np.array): scaled X.
        y (pd.df): four columns response table. 
        max_iter (int): max iteration. 
        cv (int): CV fold.
        n_threads (int): Number of threads to use for parallel computing.

    Returns:
        float: trained alpha value.

    """
    logger.info('Implementing LassoCV with {} iter. and {}-fold CV'.format(max_iter, cv))
    # generate logit response
    y_logit = logit((y.nMut + 0.5) / (y.length * y.N))
    # sub-sampling X and y (300,000)
    use_ix = np.random.choice(y_logit.shape[0], 300000, replace=False)
    Xsub = X[use_ix, :]
    ysub = y_logit[use_ix]
    reg = LassoCV(max_iter=max_iter, cv=cv, copy_X=False, n_jobs=n_threads)
    lassocv = reg.fit(Xsub, ysub)
    logger.info('LassoCV alpha = {}'.format(lassocv.alpha_))
    return lassocv.alpha_


def run_rndlasso(X, y, alpha,
    n_resampling=500, sample_fraction=0.1, n_threads=1):
    """  Implement Randomized Lasso in sklearn

    Args:
        X (np.array): scaled X. 
        y (pd.df): four columns response table. 
        alpha (float): parameter trained from lassoCV 
        n_resampling (int): number of times for resampling 
        sample_fraction (float): fraction of data to use at each resampling

    Returns:
        np.array: feature importance scores

    """
    logger.info('Implementing Randomized Lasso with alpha={}, n_resampling={} and sample_fraction={}'.
                format(alpha, n_resampling, sample_fraction))
    # generate logit response
    y_logit = logit((y.nMut + 0.5) / (y.length * y.N))
    reg = RandomizedLasso(alpha=alpha,
                          n_resampling=n_resampling,
                          sample_fraction=sample_fraction,
                          selection_threshold=1e-3,
                          max_iter=3000,
                          normalize=False,
                          n_jobs=n_threads)
    rndlasso = reg.fit(X, y_logit)
    fi_scores = rndlasso.scores_
    return fi_scores


def run_glm(X, y, model_name):
    """ Train the binomial/negative binomial GLM
    
    Args:
        X (np.array): scaled X. 
        y (pd.df): four columns response table.

    Returns:
        sm.model: trained GLM models.
        
    """
    # Add const manually. sm.add_constant cannot add 1 for shape (1, n)
    X = np.c_[X, np.ones(X.shape[0])]
    if model_name == 'Binomial':
        logger.info('Building binomial GLM')
        # make two columns response (# success, # failure)
        y_binom = np.zeros((y.shape[0], 2), dtype=np.int_)
        y_binom[:, 0] = y.nMut
        y_binom[:, 1] = y.length * y.N - y.nMut
        glm = sm.GLM(y_binom, X, family=sm.families.Binomial())
    elif model_name == 'NegativeBinomial':
        logger.info('Building negative binomial GLM')
        # use nMut as response and length*N as exposure
        glm = sm.GLM(y.nMut.values, X, family=sm.families.NegativeBinomial(), exposure=y.length.values*y.N.values+1)
    else:
        sys.stderr.write('Unknown GLM name {}. Must be Binomial or NegativeBinomial'.format(model_name))
        sys.exit(1)
    model = glm.fit()
    return model


def run_gbm(dtrain, dvalid, param):
    # check training arguments in param
    n_round = param.get('num_boost_round', 5000)
    early_stop = param.get('early_stopping_rounds', 5)
    verbose_eval = param.get('verbose_eval', 100)
    # specify validations set to watch performance
    watchlist = [(dvalid, 'eval')]
    bst = xgb.train(params=param,
                    dtrain=dtrain,
                    num_boost_round=n_round,
                    evals=watchlist,
                    early_stopping_rounds=early_stop,
                    verbose_eval = verbose_eval
                   )
    return bst


def report_metrics(yhat, y):
    # report metrics of training set
    r2 = r2_score(y, yhat)
    var_exp = explained_variance_score(y, yhat)
    r = stats.pearsonr(yhat, y)[0]
    logger.info('Model metrics for training set: r2={:.2f}, Variance explained={:.2f}, Pearson\'r={:.2f}'.format(r2, var_exp, r))


def dispersion_test(yhat, y, k=100):
    """ Implement the regression based dispersion test with k re-sampling.

    Args:
        yhat (np.array): predicted mutation count
        y (np.array): observed mutation count
        k (int):

    Returns:
        float, float: p-value, theta

    """
    theta = 0
    pval = 0
    for i in range(k):
        y_sub, yhat_sub = resample(y, yhat, random_state=i)
        # (np.power((y - yhat), 2) - y) / yhat for Poisson regression
        aux = (np.power((y_sub - yhat_sub), 2) - yhat_sub) / yhat_sub
        mod = sm.OLS(aux, yhat_sub)
        res = mod.fit()
        theta += res.params[0]
        pval += res.pvalues[0]
    theta = theta/k
    pval = pval/k
    return pval, theta
