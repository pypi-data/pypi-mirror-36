""" Data input and output module for DriverPower.

Input file types: X (tsv), y (tsv), functional scores (tsv), models (pkl)

"""
import logging
import pickle
import os
import pkg_resources
import pandas as pd
import numpy as np
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import xgboost as xgb


logger = logging.getLogger('IO')


def read_feature(path, use_features=None):
    """Read X (features) table in TSV format (or compressed).

    X must contain a column named 'binID' (key) and other columns will be treated as features.

    Args:
        path (str): Path to the file.
        use_features (list): List of features to load.

    Returns:
        pd.df: A panda DF indexed by binID.

    """
    if path.lower().endswith(('.h5', '.hdf5')):
        # HDF5
        if use_features is not None:
            X = pd.read_hdf(path, 'X')
            X = X.loc[:, use_features]
        else:
            X = pd.read_hdf(path, 'X')
    elif path.lower().endswith(('.buffer')):
        # XGBoost binary
        X = xgb.DMatrix(path)
    else:
        # TSV or compressed TSV
        if use_features is not None:
            X = pd.read_csv(path, sep='\t', header=0, index_col='binID',
                            usecols=['binID'] + use_features)
        else:
            X = pd.read_csv(path, sep='\t', header=0, index_col='binID')
    if type(X) is pd.DataFrame:
        # sanity check
        assert len(X.index.values) == len(X.index.unique()), "binID in feature table is not unique."
        na_count = X.isnull().sum()
        if na_count.sum() > 0:
            na_names = na_count.index.values[np.where(na_count>0)]
            logger.warning('NA values found in features [{}]'.format(', '.join(na_names)))
            logger.warning('Fill NA with 0')
            X.fillna(0, inplace=True)
        logger.info('Successfully load {} features for {} bins'.format(X.shape[1], X.shape[0]))
        return X
    elif type(X) is xgb.DMatrix:
        # xgb.DMatrix
        logger.info('Successfully load {} features for {} bins'.format(X.num_col(), X.num_row()))
        return X


def read_response(path):
    """Read y (response) table in TSV format.
    
    y should have exactly five columns: binID, length, nMut, nSample, N
    
    Args:
        path (str): Path to the file.
    
    Returns:
        pd.df: A panda DF indexed by binID.
        
    """
    y = pd.read_csv(path, sep='\t', header=0, index_col='binID',
                    usecols=['binID', 'length', 'nMut', 'nSample', 'N'])
    # sanity check
    assert len(y.index.values) == len(y.index.unique()), "binID in response table is not unique."
    return y


def read_fs(path, fs_cut):
    """Read functional scores table in TSV format.
    
    func_score must contain a column named 'binID' (key) and other columns will be treated as scores (one per column).
    
    Args:
        path (str): Path to the file.
        fs_cut (dict): Keys are functional score names.
    
    Returns:
        pd.df: A panda DF indexed by binID
         
    """
    fs = pd.read_csv(path, sep='\t', header=0, index_col='binID',
                     usecols=['binID'] + list(fs_cut.keys()))
    # sanity check
    assert len(fs.index.values) == len(fs.index.unique()), "binID in functional score table is not unique."
    return fs


def read_fi(path, cutoff=0.5):
    """Read feature importance table in TSV format.

    Feature importance table must contain two columns: name and importance

    Args:
        path (str): path to the file.
        cutoff (float): cutoff of feature selection.

    Returns:
        list: useful features. Return None if path is None.

    """
    if path is not None:
        fi = pd.read_csv(path, sep='\t', header=0, index_col='name',
                         usecols=['name', 'importance'])
        assert len(fi.index.values) == len(fi.index.unique()), \
            "Feature name in feature importance table is not unique."
        keep = (fi.importance >= cutoff).values
        return fi.index.values[keep].tolist()
    else:
        return None


def save_fi(fi_scores, feature_names, project_name, out_dir):
    """ Save feature importance results to disk
    
    Args:
        fi_scores (np.array): array of feature importance scores.
        feature_names (np.array): array of feature names.
        project_name (str): name of the project, prefix of the output file.
        out_dir (str): output directory. 

    Returns:
        pd.DF: feature importance table
        
    """
    res = pd.DataFrame({'name':feature_names, 'importance':fi_scores}, columns=['name', 'importance'])
    path = os.path.join(out_dir, project_name+'.feature_importance.tsv')
    res.to_csv(path, sep='\t', index=False)
    return res


def read_param(path=None):
    """ Load the parameter for xgboost.

    Args:
        path: path to the pkl file. None for default.

    Returns:
        dict: parameter dict.
    """
    # use default if path is None
    path = path if path is not None else pkg_resources.resource_filename(__name__, 'xgb_param.pkl')
    with open(path, 'rb') as f:
        param = pickle.load(f)
    return param


def save_prediction(ypred, y, project_name, out_dir, model_name):
    y['pred'] = ypred
    path = os.path.join(out_dir, '{}.{}.model.train.pred.tsv'.format(project_name, model_name))
    y.to_csv(path, sep='\t')
    return


def read_model(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


def save_model(model, project_name, out_dir, model_name):
    path = os.path.join(out_dir, '{}.{}.model.pkl'.format(project_name, model_name))
    with open(path, 'wb') as f:
        pickle.dump(model, f)


def save_result(y, project_name, out_dir):
    # sort by last but 2 column
    y = y.sort_values(y.columns[-2], ascending=True)
    path = os.path.join(out_dir, '{}.result.tsv'.format(project_name))
    y.to_csv(path, sep='\t')
