# authors: s21544 Mariusz Krzyzopolski s20499 Tomasz Baj

import argparse
import json
from operator import itemgetter
import numpy as np
from itertools import groupby


def build_arg_parser() -> argparse.ArgumentParser:
    """
    build parser of arguments to enable Euclidean and Pearson mode for certain user

    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--user', dest='user', required=True,
                        help='User')
    parser.add_argument("--score-type", dest="score_type", required=True,
                        choices=['Euclidean', 'Pearson'], help='Similarity metric to be used')
    return parser


def find_common_movies(dataset: dict, user1: str, user2: str) -> dict:
    """
    Find and return only movies rated similar by both users

    :param: user2: name of user2
    :param: user1: name of user1
    :param: dataset: dict with users movies and ratings for them
    :return: related movies
    """
    common_movies = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1
    return common_movies


def euclidean_score(dataset: dict, user1: str, user2: str) -> np.float64:
    """
    Compute the Euclidean distance score between user1 and user2

    :param: user2: name of user2
    :param: user1: name of user1
    :param: dataset: dict with users movies and ratings for them
    :return: float correlation between target users, between 1 and 0
    """
    find_common_movies(dataset, user1, user2)
    squared_diff = []
    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))
    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


def pearson_score(dataset: dict, user1: str, user2: str) -> float:
    """
    Compute the Pearson correlation score between user1 and user2

    :param: user2: name of user2
    :param: user1: name of user1
    :param: dataset: dict with users movies and ratings for them
    :return float correlation between target users, between 1 and 0
    """
    common_movies = find_common_movies(dataset, user1, user2)
    num_ratings = len(common_movies)

    # Calculate the sum of ratings of all the common movies
    user1_sum = np.sum([dataset[user1][item] for item in common_movies])
    user2_sum = np.sum([dataset[user2][item] for item in common_movies])

    # Calculate the sum of squares of ratings of all the common movies
    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in common_movies])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_movies])

    # Calculate the sum of products of the ratings of the common movies
    sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_movies])

    # Calculate the Pearson correlation score
    xy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    xx = user1_squared_sum - np.square(user1_sum) / num_ratings
    yy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if xx * yy == 0:
        return 0.0
    return xy / np.sqrt(xx * yy)


def average_duplicates(movies: list) -> list:
    """
    Find duplicate movies in list and averages the ratings

    :param: movies: list of movies, with their ratings
    :return list of movies, without duplicates and with average rating
    """
    result = []
    movies.sort(key=itemgetter(0))
    for key, value in groupby(movies, key=itemgetter(0)):
        result.append([key, np.mean(list(v[1] for v in value))])
    return result


if __name__ == '__main__':
    args = build_arg_parser().parse_args()
    user = args.user
    score_type = args.score_type
    ratings_file = 'ratings.json'
    # ratings_file = 'ratings_small.json'

    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    if user not in data:
        raise TypeError(f"Cannot find {user} in the dataset. You can choose from: {data.keys()}")

    db = []
    for other_user in data:
        # If there are no common movies between the users,
        # then skip
        distance = len(find_common_movies(data, user, other_user))
        if other_user == user or distance == 0:
            continue
        similarity_ratio = 0
        if score_type == 'Euclidean':
            similarity_ratio = euclidean_score(data, user, other_user)
        if score_type == 'Pearson':
            similarity_ratio = pearson_score(data, user, other_user)

        for movie in data[other_user]:
            if movie not in data[user].keys():
                db.append([movie, similarity_ratio * distance * data[other_user][movie]])

    db = average_duplicates(db)


    def my_func(e):
        return e[1]


    db.sort(key=my_func)

    print("Recommended movie for for you:")
    for i in db[-5:]:
        print(i[0])
    print("")
    print("You probably won't like it:")
    for i in db[:5]:
        print(i[0])
