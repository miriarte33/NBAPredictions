import numpy as numpy
import pandas as panda
import requests
from bs4 import BeautifulSoup


PER_GAME_BASE_URL = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
ADVANCED_BASE_URL = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html"
ALLSTAR_ROSTER_BASE_URL = "https://www.basketball-reference.com/allstar/NBA_{}.html"

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


def get_allstars(season: int) -> object:
    # the all star game was cancelled in 1999 due to NBA lockout
    if season == 1999:
        return panda.DataFrame()

    request_url = ALLSTAR_ROSTER_BASE_URL.format(season)
    request = requests.get(request_url)
    html_content = BeautifulSoup(request.content, "html.parser")
    west_all_stars = html_content.find("table", {"id": "West"})
    east_all_stars = html_content.find("table", {"id": "East"})

    # remove unwanted table items
    for table_head in west_all_stars("tr", {"class": "thead"}):
        table_head.decompose()
    west_all_stars.find("tr", {"class": "over_header"}).decompose()
    west_all_stars.find("tfoot").decompose()

    for table_head in east_all_stars("tr", {"class": "thead"}):
        table_head.decompose()
    east_all_stars.find("tr", {"class": "over_header"}).decompose()
    east_all_stars.find("tfoot").decompose()

    df1 = panda.read_html(str(west_all_stars))[0]
    df2 = panda.read_html(str(east_all_stars))[0]

    df2["Season"] = "{} - {}".format(season-1, season)
    df1["Season"] = "{} - {}".format(season-1, season)

    return df1.append(df2, sort=True).reset_index(drop=True).rename(columns={"Starters": "Player"})


def main():
    seasons = numpy.arange(1977, 2019, 1)

    historical_stats_data = panda.DataFrame()
    historical_all_star_data = panda.DataFrame()

    for season in seasons:
        print("Getting stats for {} - {}".format(season - 1, season))
        # get per game and advanced stats for the given season
        season_per_game_stats = get_per_game_stats(season)
        season_advanced_stats = get_advanced_stats(season)

        # merge the stats for the given season
        merged_result = panda.merge(season_per_game_stats, season_advanced_stats, on="Rk")
        merged_result["All-Star"] = 0

        # append the merged result of the season to the historical stats data
        historical_stats_data = historical_stats_data.append(merged_result).reset_index(drop=True)

    for season in seasons:
        print("Getting allstars for {} - {}".format(season-1, season))
        all_star_roster = get_allstars(season)
        historical_all_star_data = historical_all_star_data.append(all_star_roster).reset_index(drop=True)

    for i, all_star in historical_all_star_data.iterrows():
        for j, player in historical_stats_data.iterrows():
            if all_star["Player"] in player["Player"] and player["Season"] == all_star["Season"]:
                historical_stats_data.at[j, "All-Star"] = 1

    historical_stats_data.to_csv("stats_data.csv")

    return 0


if __name__ == '__main__':
    main()
