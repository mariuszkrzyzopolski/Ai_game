# authors: s21544 Mariusz Krzyzopolski s20499 Tomasz Baj

import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn.cluster import KMeans


def build_arg_parser():
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--user', dest='user', required=True,
                        help='User')
    parser.add_argument("--score-type", dest="score_type", required=True,
                        choices=['Euclidean', 'Pearson'], help='Similarity metric to be used')
    return parser


def find_common_movies(dataset, user1, user2):
    # Movies rated by both user1 and user2
    common_movies = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1
    return common_movies


# Compute the Euclidean distance score between user1 and user2
def euclidean_score(dataset, user1, user2):
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = find_common_movies(dataset, user1, user2)

    # If there are no common movies between the users,
    # then the score is 0
    if len(common_movies) == 0:
        return 0

    squared_diff = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


# Compute the Pearson correlation score between user1 and user2
def pearson_score(dataset, user1, user2):
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = find_common_movies(dataset, user1, user2)

    num_ratings = len(common_movies)

    # If there are no common movies between user1 and user2, then the score is 0
    if num_ratings == 0:
        return 0

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


def pltShow(data_frame):
    km = KMeans(n_clusters=2,
                init='random',
                n_init=10,
                max_iter=300,
                tol=1e-04,
                random_state=0)

    y_km = km.fit_predict(data_frame)
    number = max(y_km) + 1
    color = ["#" + ''.join([random.choice('0123456789ABCDEF') for i in range(6)]) for j in range(number)]

    for i in range(number):
        plt.scatter(data_frame[y_km == i, 0], data_frame[y_km == i, 1],
                    c=color[i], marker='o', s=40,
                    edgecolor='black',
                    label='Skupienie ' + str(i))

    plt.scatter(km.cluster_centers_[:, 0],
                km.cluster_centers_[:, 1],
                s=250, marker='*',
                c='red', edgecolor='black',
                label='Centroidy')
    plt.legend()
    plt.xlabel("Distanse")
    plt.ylabel("Numbers of common movie")
    plt.tight_layout()
    plt.show()


def kmeans(data, user, score_type):
    df = []
    if score_type == 'Euclidean':
        for user1 in data:
            if user1 != user:
                df.append([euclidean_score(data, user, user1), len(find_common_movies(data, user, user1))])
    if score_type == 'Pearson':
        for user1 in data:
            if user1 != user:
                df.append([pearson_score(data, user, user1), len(find_common_movies(data, user, user1))])

    df = np.array(df)

    # Loading the dataset
    plt.scatter(df[:, 0], df[:, 1], c='white', marker='o', edgecolor='black', s=50)
    plt.xlabel("Distanse")
    plt.ylabel("Numbers of common movie")
    plt.grid()
    plt.tight_layout()
    plt.show()

    pltShow(df)


def remove_duplicate(movies):
    new_db = []
    for movie in movies:
        tmp_list = []
        if movie in new_db:
            continue
        for i in movies:
            if movie[0] == i[0]:
                tmp_list.append(i)
        avg_movie = [tmp_list[0][0], 0, 0]
        for i in tmp_list:
            avg_movie[1] += i[1]
            avg_movie[2] += i[2]
        avg_movie[1] = avg_movie[1] / len(tmp_list)
        avg_movie[2] = avg_movie[2] / len(tmp_list)
        if avg_movie not in new_db:
            new_db.append(avg_movie)
    return new_db


if __name__ == '__main__':
    args = build_arg_parser().parse_args()
    user = args.user
    score_type = args.score_type
    ratings_file = 'ratings.json'
    #ratings_file = 'ratings_small.json'

    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    # kmeans(data, user, 'Euclidean')
    # kmeans(data, user, 'Pearson')
    db = []
    list_similar_users = []
    for other_user in data:
        if score_type == 'Euclidean':
            similarity_ratio = euclidean_score(data, user, other_user)
        if score_type == 'Pearson':
            similarity_ratio = pearson_score(data, user, other_user)
        distance = len(find_common_movies(data, user, other_user))
        if other_user != user and distance > 0:
            # list_similar_users.append([other_user, data[other_user], distance, match_multipiler])
            for movie in data[other_user]:
                if movie not in data[user].keys():
                    db.append([movie, data[other_user][movie], similarity_ratio * data[other_user][movie]])

    db = remove_duplicate(db)

    def myFunc(e):
        return e[2]
    db.sort(key=myFunc)
    print("good for you")
    for i in db[-5:]:
        print(i[0])
    print("don't watch")
    for i in db[:5]:
        print(i[0])


#python main.py --user 'Paweł Czapiewski' --score-type Pearson
