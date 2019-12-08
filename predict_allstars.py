import get_stats
import pandas
from sklearn import preprocessing, ensemble, metrics


def main():
    get_stats.get_stats()
    training_data = pandas.read_csv("stats_data.csv")
    training_data = training_data.drop(["Unnamed: 0"], axis="columns")

    # pre-processing must encode values because trees require categorical values to be encoded
    label_encoder = preprocessing.LabelEncoder()
    for i in range(53):
        training_data.iloc[:, i] = label_encoder.fit_transform(training_data.iloc[:, i])

    class_weight = dict({1: 1, 0: 16.5})
    forest = ensemble.RandomForestClassifier(class_weight=class_weight)

    # training
    # must drop the target variable
    # also dropping variables i dont want the forest to consider
    x_train = training_data.drop(["All-Star", "MVP-Votes", "Rk"], axis='columns')
    y_train = training_data["All-Star"]
    forest.fit(x_train, y_train)

    feature_importances = pandas.DataFrame(forest.feature_importances_, index=x_train.columns, columns=['Feature Importance']).sort_values('Feature Importance', ascending=False)
    print(feature_importances)

    # testing
    # we are now going to predict the 2017 all stars and see how well our model performed
    test_set = get_stats.create_test_set(2017)
    test_set.to_csv("data_2017.csv")

    for i in range(53):
        test_set.iloc[:, i] = label_encoder.fit_transform(test_set.iloc[:, i])

    x_test = test_set.drop(["All-Star", "MVP-Votes", "Rk"], axis='columns')
    y_test = test_set["All-Star"]

    y_predicted = forest.predict(x_test)

    print("Prediction score: {}".format(forest.score(x_test, y_test)))


if __name__ == '__main__':
    main()
