import requests
from bs4 import BeautifulSoup

from utils.logger import get_logger

logger = get_logger()


def get_nba_score():
    url = "https://www.playsport.cc/livescore.php?aid=3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

    soup = BeautifulSoup(response.content, 'html.parser')

    scores = []
    for game in soup.find_all('div', class_='outer-gamebox'):
        team1 = game.find('div', class_='big-score-s02-guest').find('h6').text
        team2 = game.find('div', class_='big-score-s02-host').find('h6').text
        score1 = game.find('div', class_='big-score-s02-guest').find('strong').text
        score2 = game.find('div', class_='big-score-s02-host').find('strong').text
        scores.append({
            'team1': team1,
            'team2': team2,
            'score1': score1,
            'score2': score2
        })

    return scores


def format_in_table_format(data):
    logger.info("formatting nba score")
    table_header = "| Team 1 | Team 2 | Score |\n| --- | --- | --- | --- |\n"
    table_rows = ""
    try:
        for game in data:
            team1 = game["team1"]
            team2 = game["team2"]
            score = f" {game['score1']} : {game['score2']}"
            table_rows += f"| {team1} | {team2} | {score} |\n"

        table_message = table_header + table_rows
    except Exception as e:
        return "Currently no game"
    return table_message


def get_nba_score_table():
    logger.info("get nba score table")
    return format_in_table_format(get_nba_score())


def get_livestream_link():
    logger.info("get nba livestream")
    return "https://stream.nbalives.tv/"


if __name__ == '__main__':
    print(get_nba_score_table())
    print(get_livestream_link())
