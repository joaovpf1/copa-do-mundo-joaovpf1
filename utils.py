from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError
from datetime import datetime


def data_processing(info):
    print(info)
    first_cup_year = int(info["first_cup"][:4])
    now_year = int(datetime.now().year)
    year_cup = []

    if info["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")

    for year in range(1930, now_year + 1, 4):
        year_cup.append(year)

    if first_cup_year not in year_cup:
        raise InvalidYearCupError("there was no world cup this year")

    if info["titles"] > (now_year - first_cup_year) // 4:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
