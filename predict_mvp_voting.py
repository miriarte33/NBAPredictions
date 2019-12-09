import get_stats
import pandas
from sklearn import preprocessing, ensemble, linear_model
import numpy


def main():
    FEATURES = ["PTS", "TRB", "AST", "Player"]
    get_stats.get_stats()
    training_data = pandas.read_csv("stats_data.csv")
    training_data_copy = training_data[FEATURES]

    label_encoder = preprocessing.LabelEncoder()
    for i in range(len(FEATURES)):
        training_data_copy.iloc[:, i] = label_encoder.fit_transform(training_data_copy.iloc[:, i])

    X_train = training_data_copy
    y_train = training_data["Share"]

    # pre-processing
    cor = training_data.corr()
    cor_target = abs(cor["Share"])
    relevant_features = cor_target[cor_target > 0.1]
    print(relevant_features)

    linear_regressor = linear_model.LinearRegression()

    linear_regressor.fit(X_train, y_train)
    print(linear_regressor.coef_)

    test_set = get_stats.create_test_set(2017)[FEATURES]
    encoded_test_set = test_set.copy()
    for i in range(len(FEATURES)):
        encoded_test_set.iloc[:, i] = label_encoder.fit_transform(encoded_test_set.iloc[:, i])

    X_test = encoded_test_set

    y_predicted = linear_regressor.predict(X_test)

    test_results = pandas.DataFrame(test_set["Player"])
    test_results["Share"] = y_predicted
    print(test_results.sort_values("Share", ascending=False)[0:10])

if __name__ == '__main__':
    main()
