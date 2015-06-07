from sklearn.metrics import classification_report, label_ranking_average_precision_score
from sklearn.preprocessing import MultiLabelBinarizer


def make_right_order(testing_problems, predicted_problems, predicted_tags):
    problem2id = {problem: i for i, problem in enumerate(testing_problems)}
    problems, tags = [0] * len(testing_problems), [0] * len(testing_problems)
    for p, t in zip(predicted_problems, predicted_tags):
        problems[problem2id[p]] = p
        tags[problem2id[p]] = t
    return problems, tags


def print_report(name_classificator, testing_problems, testing_tags, predicted_problems, predicted_tags):
    predicted_problems, predicted_tags = make_right_order(testing_problems, predicted_problems, predicted_tags)
    mlb = MultiLabelBinarizer().fit(testing_tags + predicted_tags)
    testing_tags = mlb.transform(testing_tags)
    predicted_tags = mlb.transform(predicted_tags)
    print(name_classificator)
    print(classification_report(testing_tags, predicted_tags, target_names=mlb.classes_))
    print('label ranking average precision score =',
          label_ranking_average_precision_score(testing_tags, predicted_tags))
    print('\n', ('#'*100), '\n')
