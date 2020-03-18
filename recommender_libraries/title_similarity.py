import os
import sys

import django
from django.db import connection
import numpy
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameplan_project.settings')
django.setup()
from gameplan.models import Game


class Similarity(object):
    def generate_model(self):
        data_matrix = self.import_data()
        cosine_matrix = self.make_model(data_matrix)
        return cosine_matrix, data_matrix

    @staticmethod
    def import_data():
        """ Imports the dataset and returns the resulting DataFrame matrix. """
        print("[SIM] Importing data...", sys.stdout)
        query = str(Game.objects.all().select_related().query)
        games = pandas.read_sql_query(query, connection)
        return games

    @staticmethod
    def make_model(matrix):
        """ Generates a model based on the dataset using the cosine similarity.
         :return Matrix containing the cosine similarity model. """
        print("[SIM] Creating model...", sys.stdout)
        vec = TfidfVectorizer()
        keyword_count_matrix = vec.fit_transform(numpy.asarray(matrix['ordered_keywords']))
        cos_mat = cosine_similarity(keyword_count_matrix, keyword_count_matrix)
        return cos_mat

    @staticmethod
    def make_predictions(game_id, matrix, cos_mat, n):
        """ Generates predictions given a game title, dataset matrix and cosine similarity matrix.
         :return List containing the index of each recommended game in descending order of relevance. """
        print("[SIM] Making predictions...", sys.stdout)
        indices = pandas.Series(matrix['game_id'])
        if len(indices[indices == game_id]) >= 1:
            matching_index = indices[indices == game_id].index[0]
        else:
            return list()

        scores = pandas.Series(cos_mat[matching_index]).sort_values(ascending=False)
        recommended_titles = list(scores.iloc[1:n + 1].index)

        return recommended_titles, round(scores.iloc[1:n + 1], 3)


def generate_recommendations(game_id, n):
    sim = Similarity()
    cos, data = sim.generate_model()

    prediction_indexes, scores = sim.make_predictions(game_id, data, cos, n)

    prediction_ids = list()
    for item in prediction_indexes:
        prediction_ids.append(data['game_id'].loc[item])

    return prediction_ids


if __name__ == '__main__':
    print("[SIM] Beginning recommendation process...")
    sim = Similarity()
    cos, data = sim.generate_model()

    target = Game.objects.get(game_id=11582)
    prediction_indexes, scores = sim.make_predictions(target.game_id, data, cos, 10)

    print("[SIM] Similar to " + target.title)
    for index, item in enumerate(prediction_indexes):
        print("[SIM] " + data["title"].loc[item] + ": " + str(scores.iloc[index]))
