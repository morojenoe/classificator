from .gradient_boosting import ACMClassificator
from problems2json import serialize_problems_to_file
from json2problems import deserialize_problems_from_file


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training', required=True, help='a path to a training sample')
    parser.add_argument('--testing', required=True, help='a path to a testing sample')
    parser.add_argument('--result', required=True, help='a path to result')
    args = vars(parser.parse_args())
    return args['training'], args['testing'], args['result']


def run_classification(classificator, path_to_training, path_to_testing, path_to_result):
    training_problems, training_tags = deserialize_problems_from_file(path_to_training)
    testing_problems, testing_tags = deserialize_problems_from_file(path_to_testing)

    classificator.fit(training_problems, training_tags)
    tags = classificator.predict(testing_problems)

    serialize_problems_to_file(testing_problems, tags, path_to_result)


def main(classificator):
    path_to_training, path_to_testing, path_to_result = parse_args()
    run_classification(classificator, path_to_training, path_to_testing, path_to_result)


def main_with_classificator():
    main(ACMClassificator())

if __name__ == "__main__":
    main(ACMClassificator())
