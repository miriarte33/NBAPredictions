import get_stats
import pandas


def main():
    get_stats.get_stats()
    dataframe = pandas.read_csv("stats_data.csv")

    X = dataframe.drop("MVP-Votes", 1)  # Feature Matrix
    y = dataframe["MVP-Votes"]  # Target Variable
    # pre-processing
    cor = dataframe.corr()
    cor_target = abs(cor["MVP-Votes"])
    relevant_features = cor_target[cor_target > 0.1]
    print(relevant_features)


if __name__ == '__main__':
    main()
