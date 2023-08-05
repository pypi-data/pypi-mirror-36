""" Command-line interface

Sub-commands:
    1. model - train the BMR model.
    2. infer - test for driver elements.
"""


import logging
import argparse
import os
import sys
from driverpower import __version__
from driverpower.model import run_bmr
from driverpower.infer import make_inference

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s | %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')
# create logger
logger = logging.getLogger('DP')


def get_args():
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                          argparse.MetavarTypeHelpFormatter,
                          argparse.RawDescriptionHelpFormatter):
        pass
    parser = argparse.ArgumentParser(prog='driverpower',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='DriverPower v{}: Combined burden and functional impact '
                                                 'tests for coding and non-coding cancer driver discovery.\n\n'
                                                 'See documentation and examples at '
                                                 'http://driverpower.readthedocs.io/en/latest/'.format(__version__))
    # global argument
    parser.add_argument('-v', '--version', dest='version', action="store_true",
                        help='Print the version of DriverPower')
    subparsers = parser.add_subparsers(title='The DriverPower sub-commands include',
                                       dest='subcommand')
    #
    # Background model
    #
    parser_bmr = subparsers.add_parser('model',
                                       help='Build the background mutation model',
                                       formatter_class=CustomFormatter,
                                       description='DriverPower v{}: Combined burden and functional impact '
                                                   'tests for coding and non-coding cancer driver discovery.\n\n'
                                                   'See documentation and examples at '
                                                   'http://driverpower.readthedocs.io/en/latest/'.format(__version__))
    # Input data
    dat_bmr = parser_bmr.add_argument_group(title="input data")
    dat_bmr.add_argument('--feature', dest='X_path', required=True, type=str,
                         help='Path to the training feature table')
    dat_bmr.add_argument('--response', dest='y_path', required=True, type=str,
                         help='Path to the training response table')
    dat_bmr.add_argument('--featImp', dest='fi_path', required=False, type=str,
                         help='Path to the feature importance table [optional]', default=None)
    # Parameters
    par_bmr = parser_bmr.add_argument_group(title="parameters")
    par_bmr.add_argument('--method', dest='model_name', required=True, type=str,
                         help='Algorithms to use', choices=['Binomial', 'NegativeBinomial', 'GBM'])
    par_bmr.add_argument('--featImpCut', dest='fi_cut', required=False, type=float,
                         help='Cutoff of feature importance score [optional]', default=0.5)
    par_bmr.add_argument('--gbmParam', dest='param_path', required=False, type=str,
                         help='Path to the parameter pickle [optional]', default=None)
    par_bmr.add_argument('--gbmFold', dest='kfold', required=False, type=int,
                         help='Train gbm with k-fold, k>=2 [optional]', default=3)
    par_bmr.add_argument('--predict', dest='pred', required=False, action="store_true",
                         help='Output the prediction for training set [optional]')
    par_bmr.add_argument('--name', dest='project_name', required=False, type=str,
                         help='Identifier for output files [optional]', default='DriverPower')
    par_bmr.add_argument('--modelDir', dest='out_dir', type=str,
                         help='Directory of output model files [optional]', default='./')
    #
    # Inference
    #
    parser_infer = subparsers.add_parser('infer',
                                         help='Infer driver elements',
                                         formatter_class=CustomFormatter,
                                         description = 'DriverPower v{}: Combined burden and functional impact '
                                                       'tests for coding and non-coding cancer driver discovery.\n\n'
                                                       'See documentation and examples at '
                                                       'http://driverpower.readthedocs.io/en/latest/'.format(__version__))
    # Input data
    dat_infer = parser_infer.add_argument_group(title="input data")
    dat_infer.add_argument('--feature', dest='X_path', required=True, type=str,
                           help='Path to the test feature table')
    dat_infer.add_argument('--response', dest='y_path', required=True, type=str,
                           help='Path to the test response table')
    dat_infer.add_argument('--model', dest='model_path', required=True, type=str,
                           help='Path to the model pickle')
    dat_infer.add_argument('--funcScore', dest='fs_path', required=False, type=str,
                           help='Path to the functional score table [optional]', default=None)
    # Parameters
    par_infer = parser_infer.add_argument_group(title="parameters")
    par_infer.add_argument('--method', dest='test_method', required=False, type=str,
                           help='Test method to use [optional]', choices=['auto', 'binomial', 'negative_binomial'], default='auto')
    par_infer.add_argument('--scale', dest='scale', required=False, type=float,
                           help='Scaling factor for theta in negative binomial distribution [optional]', default=1)
    par_infer.add_argument('--funcScoreCut', dest='fs_cut', required=False, type=str,
                           help='Score name:cutoff pairs for all scores e.g.,'
                                '"CADD:0.01,DANN:0.03,EIGEN:0.03" [optional]',
                           default=None)
    par_infer.add_argument('--geoMean', dest='use_gmean', required=False, type=bool,
                           help='Use geometric mean in test [optional]', default=True)
    par_infer.add_argument('--name', dest='project_name', required=False, type=str,
                           help='Identifier for output files [optional]', default=None)
    par_infer.add_argument('--outDir', dest='out_dir', type=str,
                           help='Directory of output files [optional]', default='./')
    args = parser.parse_args()
    ###
    # Check and modify args
    ###
    if len(sys.argv) == 1:
        # print help when no argument
        parser.print_help()
        sys.exit(1)
    if hasattr(args, 'out_dir'):
        args.out_dir = os.path.abspath(args.out_dir)
    return args


def main():
    args = get_args()
    logger.info('Welcome to DriverPower v{}'.format(__version__))
    if args.subcommand == 'model':
        run_bmr(model_name=args.model_name,
                X_path=args.X_path,
                y_path=args.y_path,
                fi_cut=args.fi_cut,
                fi_path=args.fi_path,
                kfold=args.kfold,
                save_pred=args.pred,
                param_path=args.param_path,
                project_name=args.project_name,
                out_dir=args.out_dir)
    elif args.subcommand == 'infer':
        make_inference(model_path=args.model_path,
                       X_path=args.X_path,
                       y_path=args.y_path,
                       fs_path=args.fs_path,
                       fs_cut=args.fs_cut,
                       test_method=args.test_method,
                       scale=args.scale,
                       use_gmean=args.use_gmean,
                       project_name=args.project_name,
                       out_dir=args.out_dir)


if __name__ == '__main__':
    main()
