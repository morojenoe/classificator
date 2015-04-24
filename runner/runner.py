from path import Path
import sys
sys.path.append(Path().getcwd().parent)

from database import get_learning_set
from sklearn.cross_validation import train_test_split


def load_set_from_file():
    return []


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='append', required=True,
                        help='is the command you would use to execute your classificator')
    parser.add_argument('-l', help='a path to a learning sample')
    parser.add_argument('-t', help='a path to a testing sample')
    args = vars(parser.parse_args())
    return args['c'], args['l'], args['t']


if __name__ == "__main__":
    classificators, learning, testing = parse_args()
    if learning is None:
        learning_problems, learning_tags = get_learning_set()
    else:
        learning_problems, learning_tags = load_set_from_file(learning)

    if testing is None:
        learning_problems, test_problems, learning_tags, test_tags = train_test_split(learning_problems,
                                                                                      learning_tags,
                                                                                      test_size=0.3)
    else:
        test_problems, test_tags = load_set_from_file(testing)
