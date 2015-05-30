# import sys
# from path import Path
# sys.path.append(Path().getcwd().parent)

import logging
from .db import get_training_set as get_training_set_from_db
from .report import print_report
from sklearn.cross_validation import train_test_split
from problems2json import serialize_problems_to_file
from json2problems import deserialize_problems_from_file
from path import Path
import subprocess


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='append', required=True,
                        help='is the command you would use to execute your classificator')
    parser.add_argument('--training', help='a path to a training sample')
    parser.add_argument('--testing', help='a path to a testing sample')
    args = vars(parser.parse_args())
    return args['c'], args['training'], args['testing']


def get_free_files():
    return Path('training.dat').abspath(), Path('testing.dat').abspath(), Path('result.dat').abspath()


def get_training_set(path_to_training):
    return get_training_set_from_db() if path_to_training is None else deserialize_problems_from_file(path_to_training)


def get_testing_set(path_to_testing, training_problems, training_tags):
    if path_to_testing is None:
        return train_test_split(training_problems, training_tags, test_size=0.4)
    testing_problems, testing_tags = deserialize_problems_from_file(path_to_testing)
    return training_problems, testing_problems, training_tags, testing_tags


def run_classification(classificators, path_to_training, path_to_testing):
    training_problems, training_tags = get_training_set(path_to_training)
    training_problems, testing_problems, training_tags, testing_tags = get_testing_set(path_to_testing,
                                                                                       training_problems, training_tags)
    path_to_training, path_to_testing, path_to_result = get_free_files()

    serialize_problems_to_file(training_problems, training_tags, path_to_training)
    serialize_problems_to_file(testing_problems, testing_tags, path_to_testing)

    for classificator in classificators:
        cmd = classificator.split(' ')
        cmd.extend(['--training', path_to_training, '--testing', path_to_testing, '--result', path_to_result])
        child = subprocess.Popen(cmd)
        return_code = child.wait()
        if return_code != 0:
            logging.error('The command "{0}" returned a non-zero code'.format(' '.join(cmd)))
        else:
            predicted_problems, predicted_tags = deserialize_problems_from_file(path_to_result)
            print_report(testing_problems, testing_tags, predicted_problems, predicted_tags)

    path_to_result.remove_p()
    path_to_training.remove()
    path_to_testing.remove()

def main():
    classificators, path_to_training, path_to_testing = parse_args()
    run_classification(classificators, path_to_training, path_to_testing)
