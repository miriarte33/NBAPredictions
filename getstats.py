import numpy as numpy
import pandas as panda
import requests
from bs4 import BeautifulSoup


PER_GAME_BASE_URL = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
ADVANCED_BASE_URL = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html"


def get_per_game_stats(season: int) -> object:
    request_url = PER_GAME_BASE_URL.format(season)
    request = requests.get(request_url)
    html_content = BeautifulSoup(request.content, "html.parser")
    table = html_content.find("table", {"id": "per_game_stats"})
    # remove unwanted table headings that appear mid-table
    for table_head in table("tr", {"class": "thead"}):
        table_head.decompose()

    df = panda.read_html(str(table))[0]
    df["Season"] = "{} - {}".format(season-1, season)
    df = df.drop_duplicates(subset="Rk")

    return df


def get_advanced_stats(season: int) -> object:
    request_url = ADVANCED_BASE_URL.format(season)
    request = requests.get(request_url)
    html_content = BeautifulSoup(request.content, "html.parser")
    table = html_content.find("table", {"id": "advanced_stats"})
    # remove unwanted table headings that appear mid-table
    for table_head in table("tr", {"class": "thead"}):
        table_head.decompose()

    df = panda.read_html(str(table))[0]

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.drop_duplicates(subset="Rk")
    # remove duplicate columns found in the per game status
    df = df.drop(["Pos", "Age", "Tm", "G", "MP", "Player"], axis=1)

    return df


def main():
    seasons = numpy.arange(1977, 2019, 1)

    historical_data = panda.DataFrame()

    for season in seasons:
        print("Getting stats for {} - {}".format(season - 1, season))
        # get per game and advanced stats for the given season
        season_per_game_stats = get_per_game_stats(season)
        season_advanced_stats = get_advanced_stats(season)

        # merge the stats for the given season
        merged_result = panda.merge(season_per_game_stats, season_advanced_stats, on="Rk")

        # append the merged result of the season to the historical data
        historical_data = historical_data.append(merged_result)

    historical_data.to_csv("stats_data.csv")

    return 0


if __name__ == '__main__':
    main()
