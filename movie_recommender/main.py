# authors: s21544 Mariusz Krzyzopolski s20499 Tomasz Baj

import argparse
import json
import numpy as np


def build_arg_parser():
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--user', dest='user', required=True,
                        help='User')
    parser.add_argument("--score-type", dest="score_type", required=True,
                        choices=['Euclidean', 'Pearson'], help='Similarity metric to be used')
    return parser


# Find common movies
def find_common_movies(dataset, user1, user2):
    # Movies rated by both user1 and user2
    common_movies = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1
    return common_movies


# Compute the Euclidean distance score between user1 and user2
def euclidean_score(dataset, user1, user2):
    common_movies = find_common_movies(dataset, user1, user2)
    squared_diff = []
    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))
    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


# Compute the Pearson correlation score between user1 and user2
def pearson_score(dataset, user1, user2):
    # Movies rated by both user1 and user2
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
    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


# Find duplicate movies in list and averages the ratings
def average_duplicates(movies):
    new_db = []
    for movie in movies:
        tmp_list = []
        if movie in new_db:
            continue
        for i in movies:
            if movie[0] == i[0]:
                tmp_list.append(i)
        avg_movie = [tmp_list[0][0], 0]
        for i in tmp_list:
            avg_movie[1] += i[1]
        avg_movie[1] = avg_movie[1] / len(tmp_list)
        if avg_movie not in new_db:
            new_db.append(avg_movie)
    return new_db


if __name__ == '__main__':
    args = build_arg_parser().parse_args()
    user = args.user
    score_type = args.score_type
    ratings_file = 'ratings.json'
    # ratings_file = 'ratings_small.json'

    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    if user not in data:
        raise TypeError('Cannot find ' + user + ' in the dataset')

    db = []
    for other_user in data:
        similarity_ratio = 0
        if score_type == 'Euclidean':
            similarity_ratio = euclidean_score(data, user, other_user)
        if score_type == 'Pearson':
            similarity_ratio = pearson_score(data, user, other_user)
        distance = len(find_common_movies(data, user, other_user))

        # If there are no common movies between the users,
        # then skip
        if other_user == user or distance == 0:
            continue

        for movie in data[other_user]:
            if movie not in data[user].keys():
                db.append([movie, similarity_ratio * distance * data[other_user][movie]])

    db = average_duplicates(db)


    def myFunc(e):
        return e[1]


    db.sort(key=myFunc)

    print("Recomended movie for for you:")
    for i in db[-5:]:
        print(i[0])
    print("")
    print("You probably won't like it:")
    for i in db[:5]:
        print(i[0])

# python main.py --user 'Paweł Czapiewski' --score-type Euclidean
