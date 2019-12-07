import get_stats
import numpy
import pandas
from sklearn import tree, preprocessing, ensemble


def main():
    get_stats.get_stats()
    dataframe = pandas.read_csv("stats_data.csv")

    # pre-processing must encode values because cannot fit strings
    label_encoder = preprocessing.LabelEncoder()
    for i in range(54):
        dataframe.iloc[:, i] = label_encoder.fit_transform(dataframe.iloc[:, i])

    forest = ensemble.ExtraTreesClassifier(n_estimators=250, random_state=0)

    # must drop the target variable
    # also dropping variables i dont want the forest to consider
    x = dataframe.drop(["All-Star", "MVP-Votes", "Unnamed: 0", "Rk"], axis='columns')
    y = dataframe["All-Star"]
    forest.fit(x, y)

    feature_importances = pandas.DataFrame(forest.feature_importances_, index=x.columns, columns=['Feature Importance']).sort_values('Feature Importance', ascending=False)
    print(feature_importances)


if __name__ == '__main__':
    main()
