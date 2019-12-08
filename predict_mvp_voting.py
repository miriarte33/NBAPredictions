import get_stats
import pandas
import numpy
from sklearn import preprocessing, ensemble, metrics, linear_model
import matplotlib.pyplot as plot


def main():
    get_stats.get_stats()
    training_data = pandas.read_csv("stats_data.csv")
    training_data = training_data.drop(["Unnamed: 0"], axis="columns")

    # pre-processing must encode values because trees require categorical values to be encoded
    # adding weight to the negative class to solve the class imbalance issue
    label_encoder = preprocessing.LabelEncoder()
    for i in range(53):
        training_data.iloc[:, i] = label_encoder.fit_transform(training_data.iloc[:, i])

    forest = ensemble.RandomForestRegressor(n_estimators=100)

    # training
    # must drop the target variable
    # also dropping variables i dont want the forest to consider
    x_train = training_data.drop(["Share", "Rk"], axis='columns')
    y_train = training_data["Share"]

    forest.fit(x_train, y_train)

    feature_importances = pandas.DataFrame(forest.feature_importances_, index=x_train.columns, columns=['Feature Importance']).sort_values('Feature Importance', ascending=False)
    print(feature_importances)

    # testing
    # we are now going to predict the 2017 all stars and see how well our model performed
    test_set = get_stats.create_test_set(2017)
    encoded_test_set = test_set.copy()
    for i in range(forest.n_features_):
        encoded_test_set.iloc[:, i] = label_encoder.fit_transform(encoded_test_set.iloc[:, i])

    x_test = encoded_test_set.drop(["Share", "Rk"], axis='columns')

    y_predicted = forest.predict(x_test)

    print("\nPredicted MVP Votes: ")
    count = 1
    for i, player in test_set.iterrows():
        if y_predicted[i] > 0:
            print("{}. {} Votes: {}".format(count, player["Player"], y_predicted[i]))
            count += 1


if __name__ == '__main__':
    main()
