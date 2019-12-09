import get_stats
import pandas
from sklearn import preprocessing, ensemble, metrics, linear_model,tree, svm
import numpy


def run_regression(features = None):
    get_stats.get_stats()

    training_data = pandas.read_csv("stats_data.csv")

    training_data.fillna(0, inplace=True)
    if features is None:    
        features = training_data.copy().drop(["Share", "Unnamed: 0"], axis="columns").columns

    training_data_copy = training_data[features]

    label_encoder = preprocessing.LabelEncoder()
    for i in range(len(features)):
        training_data_copy.iloc[:, i] = label_encoder.fit_transform(training_data_copy.iloc[:, i])

    X_train = training_data_copy
    y_train = training_data["Share"]

    decision_tree = tree.DecisionTreeRegressor()

    decision_tree.fit(X_train, y_train)

    test_set = get_stats.create_test_set(2017)
    test_set_copy = test_set[features]
    encoded_test_set = test_set_copy
    for i in range(len(features)):
        encoded_test_set.iloc[:, i] = label_encoder.fit_transform(encoded_test_set.iloc[:, i])

    X_test = encoded_test_set
    y_test = encoded_test_set["All-Star"]

    y_predicted = decision_tree.predict(X_test)

    print("\nDecision Tree Regressor Results: ")
    test_results = pandas.DataFrame(test_set["Player"])
    test_results["Share"] = y_predicted
    print(test_results.sort_values("Share", ascending=False)[0:10])
    print("Mean Absolute Error: {}".format(metrics.mean_absolute_error(y_test, y_predicted)))
    print("Mean Squared Error: {}".format(metrics.mean_squared_error(y_test, y_predicted)))
    print("R2 Score: {}".format(metrics.r2_score(y_test, y_predicted)))

    forest = ensemble.RandomForestRegressor(random_state=3)

    forest.fit(X_train, y_train)

    test_set = get_stats.create_test_set(2017)
    test_set_copy = test_set[features]
    encoded_test_set = test_set_copy
    for i in range(len(features)):
        encoded_test_set.iloc[:, i] = label_encoder.fit_transform(encoded_test_set.iloc[:, i])

    X_test = encoded_test_set
    y_test = encoded_test_set["All-Star"]

    y_predicted = forest.predict(X_test)

    print("\nRandom Forest Regressor Results: ")
    test_results = pandas.DataFrame(test_set["Player"])
    test_results["Share"] = y_predicted
    print(test_results.sort_values("Share", ascending=False)[0:10])
    print("Mean Absolute Error: {}".format(metrics.mean_absolute_error(y_test, y_predicted)))
    print("Mean Squared Error: {}".format(metrics.mean_squared_error(y_test, y_predicted)))
    print("R2 Score: {}".format(metrics.r2_score(y_test, y_predicted)))

    linear = linear_model.LinearRegression()

    linear.fit(X_train, y_train)

    test_set = get_stats.create_test_set(2017)
    test_set_copy = test_set[features]
    encoded_test_set = test_set_copy
    for i in range(len(features)):
        encoded_test_set.iloc[:, i] = label_encoder.fit_transform(encoded_test_set.iloc[:, i])

    X_test = encoded_test_set
    y_test = encoded_test_set["All-Star"]

    y_predicted = linear.predict(X_test)

    print("\nLinear Multivariate Regressor Results: ")
    test_results = pandas.DataFrame(test_set["Player"])
    test_results["Share"] = y_predicted
    print(test_results.sort_values("Share", ascending=False)[0:10])
    print("Mean Absolute Error: {}".format(metrics.mean_absolute_error(y_test, y_predicted)))
    print("Mean Squared Error: {}".format(metrics.mean_squared_error(y_test, y_predicted)))
    print("R2 Score: {}".format(metrics.r2_score(y_test, y_predicted)))


def main():
    features = ["PTS", "TRB", "AST", "All-Star", "FGA", "WS", "FG%"]
    print("\nRegression With All Features: ")
    run_regression()

    print("\nRegression with Subset of Features {}".format(features))
    run_regression(features)


if __name__ == '__main__':
    main()
