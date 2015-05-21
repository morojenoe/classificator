import sys
from path import Path
sys.path.append(Path().getcwd().parent)

from db import get_training_set as get_training_set_from_db
from sklearn.cross_validation import train_test_split
from problems2json import serialize_problems_to_file
from json2problems import deserialize_problems_from_file
import subprocess


def load_problems_from_file(path_to_file):
    return deserialize_problems_from_file(path_to_file)


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
    return 'training.dat', 'testing.dat', 'result.dat'


def get_training_set(path_to_training):
    return get_training_set_from_db() if path_to_training is None else load_problems_from_file(path_to_training)


def get_testing_set(path_to_testing, training_problems, training_tags):
    if path_to_testing is None:
        return train_test_split(training_problems, training_tags, test_size=0.4)
    testing_problems, testing_tags = load_problems_from_file(path_to_testing)
    return training_problems, testing_problems, training_tags, testing_tags


def main(classificators, path_to_training, path_to_testing):
    training_problems, training_tags = get_training_set(path_to_training)
    training_problems, testing_problems, training_tags, testing_tags = get_testing_set(path_to_testing,
                                                                                       training_problems, training_tags)
    path_to_training, path_to_testing, path_to_result = get_free_files()

    serialize_problems_to_file(training_problems, training_tags, path_to_training)
    serialize_problems_to_file(testing_problems, testing_tags, path_to_testing)

    for classificator in classificators:
        cmd = classificator.split(' ')
        cmd.extend(['--training', path_to_training, '--testing', path_to_testing, '--result', path_to_result])
        subprocess.Popen(cmd)


if __name__ == "__main__":
    classificators, path_to_training, path_to_testing = parse_args()
    main(classificators, path_to_training, path_to_testing)
