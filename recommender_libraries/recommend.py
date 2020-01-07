import json
import os
import sys

import django
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
import numpy
import pandas
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender_libraries.lib.rake import Rake

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameplan_project.settings')
django.setup()
from gameplan.models import Game


class Similarity(object):

    def __init__(self):
        self.rake = Rake()

    def generate_model(self):
        data_matrix = self.__import_data()
        cosine_matrix = self.__make_model(data_matrix)
        return cosine_matrix, data_matrix

    @staticmethod
    def __import_data():
        """ Imports the dataset and returns the resulting DataFrame matrix. """
        print("Importing data...")
        query = str(Game.objects.all().query)
        games = pandas.read_sql_query(query, connection)
        return games

    @staticmethod
    def __make_model(matrix):
        """ Generates a model based on the dataset using the cosine similarity.
         :return Matrix containing the cosine similarity model. """
        print("Creating model...")
        vec = TfidfVectorizer()
        keyword_count_matrix = vec.fit_transform(numpy.asarray(matrix["ordered_keywords"]))
        cos_mat = cosine_similarity(keyword_count_matrix, keyword_count_matrix)
        return cos_mat

    def make_predictions(self, title, matrix, cos_mat, n):
        """ Generates predictions given a film title, dataset matrix and cosine similarity matrix.
         :return List containing the index of each recommended game in descending order of relevance. """
        print("Making predictions...")
        indices = pandas.Series(matrix["title"])
        if len(indices[indices == title]) >= 1:
            matching_index = indices[indices == title].index[0]
        else:
            return list()

        scores = pandas.Series(cos_mat[matching_index]).sort_values(ascending=False)
        recommended_titles = list(scores.iloc[1:n + 1].index)

        predictions = dict()
        for i in range(0, len(recommended_titles) - 1):
            predictions[i] = (matrix.loc[recommended_titles[i]]).to_dict()

        return predictions


def generate_recommendations(title, n):
    sim = Similarity()
    cos, data = sim.generate_model()
    predictions = sim.make_predictions(title, data, cos, n)

    return predictions


if __name__ == '__main__':
    print("Beginning recommendation process...")
    sim = Similarity()
    cos, data = sim.recalculate_model()
    prediction_ids = sim.make_predictions("Call Of Duty: Modern Warfare", data, cos, 10)

    print("Recommendations: ")
    for item in prediction_ids:
        print(data["title"].loc[item])
