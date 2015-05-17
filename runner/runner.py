from path import Path
import sys
sys.path.append(Path().getcwd().parent)

from db import get_learning_set
from sklearn.cross_validation import train_test_split


def load_set_from_file():
    return []


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='append', required=True,
                        help='is the command you would use to execute your classificator')
    parser.add_argument('--training', help='a path to a training sample')
    parser.add_argument('--testing', help='a path to a testing sample')
    args = vars(parser.parse_args())
    return args['c'], args['training'], args['testing']


if __name__ == "__main__":
    classificators, training, testing = parse_args()
    if training is None:
        training_problems, training_tags = get_learning_set()
    else:
        training_problems, training_tags = load_set_from_file(training)

    if testing is None:
        training_problems, test_problems, training_tags, test_tags = train_test_split(training_problems,
                                                                                      training_tags,
                                                                                      test_size=0.4)
    else:
        test_problems, test_tags = load_set_from_file(testing)
