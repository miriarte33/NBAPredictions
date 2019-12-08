import get_stats
import pandas
from sklearn import preprocessing, ensemble, linear_model
import numpy


def main():
    get_stats.get_stats()
    training_data = pandas.read_csv("stats_data.csv")
    training_data = training_data.drop(["Unnamed: 0", "FGA", "2PA", "3PA", "3PAr", "FTA", "ORB", "DRB", "OWS", "DWS"], axis="columns")
    training_data["3P"].fillna(0)
    training_data["3P%"].fillna(0)
    mean_tov = training_data["TOV"].mean
    training_data["TOV"].fillna(mean_tov)
    mean_tov_percentage = training_data["TOV%"].mean
    training_data["TOV%"].fillna(mean_tov_percentage)
    mean_usg = training_data["USG%"].mean
    training_data["USG%"].fillna(mean_usg)
    mean_gs = training_data["GS"].mean
    training_data["GS"].fillna(mean_gs)

    label_encoder = preprocessing.LabelEncoder()
    for i in range(42):
        training_data.iloc[:, i] = label_encoder.fit_transform(training_data.iloc[:, i])

    X_train = training_data.drop("Share", axis="columns")
    y_train = training_data["Share"]

    # pre-processing
    cor = training_data.corr()
    cor_target = abs(cor["Share"])
    relevant_features = cor_target[cor_target > 0.1]
    print(relevant_features)

    linear_regressor = linear_model.LinearRegression()

    linear_regressor.fit(X_train, y_train)
    print(linear_regressor.coef_)

    test_set = get_stats.create_test_set(2017).drop(["FGA", "2PA", "3PA", "3PAr", "FTA", "ORB", "DRB", "OWS", "DWS"], axis="columns")
    encoded_test_set = test_set.copy()
    for i in range(42):
        encoded_test_set.iloc[:, i] = label_encoder.fit_transform(encoded_test_set.iloc[:, i])

    X_test = encoded_test_set.drop(["Share"], axis='columns')
    y_test = encoded_test_set["Share"]

    y_predicted = linear_regressor.predict(X_test)

    test_results = pandas.DataFrame(test_set["Player"])
    test_results["Share"] = y_predicted
    print(test_results.sort_values("Share", ascending=False)[0:10])

if __name__ == '__main__':
    main()
