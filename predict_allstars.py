import get_stats
import pandas
import numpy
from sklearn import preprocessing, ensemble, metrics
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
    encoded_test_set = test_set.copy()
    for i in range(forest.n_features_):
        encoded_test_set.iloc[:, i] = label_encoder.fit_transform(encoded_test_set.iloc[:, i])

    x_test = encoded_test_set.drop(["All-Star", "MVP-Votes", "Rk"], axis='columns')
    y_test = encoded_test_set["All-Star"]

    # increasing the classification threshold to try to force our model to picking closer to 24 all stars, the real life amount
    y_predicted_probabilities = forest.predict_proba(x_test)[:, 1]
    # need to reshape the data to a 2D array. -1, 1 means there is only one feature
    y_predicted = preprocessing.binarize(y_predicted_probabilities.reshape(-1, 1), 0.43)

    print("\nPredicted All Stars: ")
    count = 1
    for i, player in test_set.iterrows():
        if y_predicted[i] == 1:
            print("{}. {}".format(count, player["Player"]))
            count += 1

    print("\nConfusion Matrix:")
    print(metrics.confusion_matrix(y_test, y_predicted))

    print("\nAccuracy: {}".format(metrics.accuracy_score(y_test, y_predicted)))
    print("\nPrecision: {}".format(metrics.precision_score(y_test, y_predicted)))
    print("\nRecall: {}".format(metrics.recall_score(y_test, y_predicted)))
    print("\nF Measure: {}".format(metrics.f1_score(y_test, y_predicted)))
    print ("\nAUC: {}".format(metrics.roc_auc_score(y_test, y_predicted_probabilities)))

    false_positive_rate, true_positive_rate, thresholds = metrics.roc_curve(y_test, y_predicted_probabilities)

    plot.plot(false_positive_rate, true_positive_rate)
    plot.xlim([0.0, 1.0])
    plot.ylim([0.0, 1.0])
    for x, y, txt in zip(false_positive_rate[::5], true_positive_rate[::5], thresholds[::5]):
        plot.annotate(numpy.round(txt, 2), (x, y - 0.04))
    plot.rcParams['font.size'] = 8
    plot.title('ROC curve for All Star classifier')
    plot.xlabel('False Positive Rate')
    plot.ylabel('True Positive Rate')
    plot.grid(True)
    plot.show()


if __name__ == '__main__':
    main()
