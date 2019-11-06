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
    df["Season"] = "{} - {}".format(season-1, season)
    return df


def main():
    seasons = numpy.arange(1977, 2019, 1)

    per_game_stats = panda.DataFrame()
    advanced_stats = panda.DataFrame()

    for season in seasons:
        print("Getting stats for {} - {}".format(season - 1, season))
        # get per game and advanced stats for the given season
        season_per_game_stats = get_per_game_stats(season)
        season_advanced_stats = get_advanced_stats(season)

        # append them to the data frame
        per_game_stats = per_game_stats.append(season_per_game_stats)
        advanced_stats = advanced_stats.append(season_advanced_stats)

    per_game_stats.to_csv("per_game_stats_data.csv")
    advanced_stats.to_csv("advanced_stats_data.csv")

    return 0


if __name__ == '__main__':
    main()
