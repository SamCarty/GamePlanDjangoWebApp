import os
import django
import pandas
from django.db import connection
from sklearn.feature_extraction.text import TfidfVectorizer

import plotly.express as px
import numpy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import average_precision_score

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameplan_project.settings')
django.setup()

from recommender.views import users_like_you
from recommender_libraries.title_similarity import generate_recommendations

from django.contrib.auth.models import User
from gameplan.models import Game
from gatherer.models import Log


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
        precisions = list()
        for user in users:
            print(user.username)
            user_recs = users_like_you(user.id, 8)
            confidences = user_recs['confidence']
            recs = user_recs['data']

            game_ids = list()
            for rec in recs:
                game_ids.append(rec['game_id'])

            if len(game_ids) > 0:
                ils.append(self.calculate_intra_list_similarity(game_ids))
                precisions.append(self.calculate_precision(user.id, game_ids, confidences))
                for g_id in game_ids:
                    recommendations.append(g_id)

        coverage = self.calculate_coverage(len(list(get_all_games())), recommendations)
        intra = round(numpy.mean(ils) * 100, 3)
        precision = round(numpy.mean(precisions) * 1, 3)
        return coverage, intra, precision

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

    def calculate_precision(self, user_id, game_ids, confidences):
        success_games = set(Log.objects.filter(user_id=user_id, event_type='detail_view_event').values_list('content_id', flat=True))

        truth = list()
        for i in range(0, len(game_ids)):
            truth.append(1) if game_ids[i] in success_games else truth.append(0)

        avg_precision = average_precision_score(truth, confidences)
        print(avg_precision)
        if numpy.isnan(avg_precision):
            avg_precision = 0.0

        return avg_precision

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
    print('Calculating... This might take a while!')
    if i == '1':
        coverage_val, intra_val= eval.evaluate_content_based()
    else:
        coverage_val, intra_val, precision_val = eval.evaluate_collaborative()
        print("Precision: " + str(precision_val))

    print("Coverage: " + str(coverage_val) + "%")
    print("Intra-list similarity: " + str(intra_val) + "%")
