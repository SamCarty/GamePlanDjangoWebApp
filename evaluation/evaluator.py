import os
import django
import pandas
from django.db import connection
from sklearn.feature_extraction.text import TfidfVectorizer

import plotly.express as px
from sklearn.metrics import pairwise_distances
import numpy
from sklearn.metrics.pairwise import cosine_similarity

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameplan_project.settings')
django.setup()

from recommender.views import users_like_you
from recommender_libraries.title_similarity import generate_recommendations

from django.contrib.auth.models import User
from gameplan.models import Game


def get_game_query_by_id_list(game_ids):
    return Game.objects.filter(game_id__in=game_ids).values('ordered_keywords').query


def get_all_games():
    return Game.objects.all()


def get_all_users():
    return User.objects.all()


class Evaluator:

    def evaluate_collaborative(self):
        users = list(get_all_users())
        recommendations = list()
        ils = list()
        for user in users:
            print(user.username)
            recs = users_like_you(user.id, 50)
            recs = recs['data']
            recs = [rec['game_id'] for rec in recs]

            if len(recs) > 0:
                intra = self.calculate_intra_list_similarity(recs)
                ils.append(intra)
                for rec in recs:
                    recommendations.append(rec)

        coverage = self.calculate_coverage(len(list(get_all_games())), recommendations)
        intra = round(numpy.mean(ils) * 100, 3)
        return coverage, intra

    def evaluate_content_based(self):
        games = list(get_all_games())
        recommendations = list()
        ils = list()
        for game in games:
            print(game.title)
            recs = generate_recommendations(game.game_id, 50)

            intra = self.calculate_intra_list_similarity(recs)
            ils.append(intra)

            for rec in recs:
                recommendations.append(rec)

        self.plot_recs(recommendations)
        coverage = self.calculate_coverage(len(list(games)), recommendations)
        intra = round(numpy.mean(ils) * 100, 2)
        return coverage, intra

    def calculate_coverage(self, games_len, recs):
        # remove duplicate values
        recommendations = list(dict.fromkeys(recs))

        # calculate the coverage
        coverage = round((len(recommendations) / games_len) * 100, 2)

        return coverage

    def calculate_intra_list_similarity(self, recs):
        query = str(get_game_query_by_id_list(recs))
        if query is not None:
            keywords = pandas.read_sql_query(query, connection)

            vec = TfidfVectorizer()
            keyword_count_matrix = vec.fit_transform(numpy.asarray(keywords['ordered_keywords']))
            similarity = cosine_similarity(keyword_count_matrix, keyword_count_matrix)

            sum = numpy.sum(similarity)

            n = numpy.size(similarity) - len(numpy.diag(similarity))

            intra = sum / n

            return intra

    def plot_recs(self, recs):
        unique, c = numpy.unique(recs, return_counts=True)
        counts = dict(zip(unique, c))

        recs_df = pandas.DataFrame()
        recs_df['game_id'] = counts.keys()
        recs_df['count'] = counts.values()
        recs_df.sort_values(by='count', inplace=True, ascending=False)
        recs_df = recs_df.reset_index()
        print(recs_df)

        fig = px.bar(recs_df, x=recs_df.index, y='count', hover_data=['game_id'])
        fig = fig.update_layout(xaxis={'categoryorder': 'total descending'})
        fig.show()


if __name__ == '__main__':
    print('[EVAL] Content-based or collaborative?')
    eval = Evaluator()
    i = input("Press [1] for content-based. \nPress [2] for collaborative.")
    if i == '1':
        print('Calculating... This takes a while!')
        coverage_val, intra_val = eval.evaluate_content_based()
    else:
        print('Calculating...')
        coverage_val, intra_val = eval.evaluate_collaborative()

    print("Coverage: " + str(coverage_val) + "%")
    print("Intra-list similarity: " + str(intra_val) + "%")
