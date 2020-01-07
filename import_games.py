import json
import os
from functools import reduce

import django
import pandas
from django.db import connection

from recommender_libraries.lib.rake import Rake

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameplan_project.settings')
django.setup()

from gameplan.models import Game, Genre


def clear_database():
    print("Purging all Game entries in database.")
    Game.objects.all().delete()
    Genre.objects.all().delete()
    print("Purge complete.")


def import_file(filename):
    with open(filename, encoding='utf-8') as file:
        data = json.loads(file.read())

        game_data = data['games']
        games = list()
        for i in range(0, len(game_data)-1):
            game = game_data[i]
            print("Adding game: " + game['name'])

            game_object = Game.objects.create(game_id=game['id'], title=game['name'])

            if 'summary' in game:
                game_object.summary = game['summary']

            if 'storyline' in game:
                game_object.storyline = game['storyline']

            if 'genres' in game:
                for genre in game['genres']:
                    genre = Genre.objects.get_or_create(genre_id=genre['id'], name=genre['name'])[0]
                    game_object.genres.add(genre)

            game_object.save()
            games.append(game_object)

        print(str(len(games)) + " items added to database.")
        return games


def combine_dbs():
    """ Imports the dataset and returns the resulting DataFrame matrix. """
    print("Combining databases...")
    query = str(Game.objects.all().query)
    games = pandas.read_sql_query(query, connection)

    query = str(Game.genres.through.objects.all().query)
    genres = pandas.read_sql_query(query, connection)

    query = str(Genre.objects.all().query)
    genre_names = pandas.read_sql_query(query, connection)

    genres = pandas.merge(genres, genre_names, on='genre_id', how='outer')

    pandas.options.display.width = 0
    games = reduce(lambda x, y: pandas.merge(x, y, on='game_id', how='outer'), [games, genres])
    games = games.fillna('').groupby(['game_id', 'title', 'summary', 'storyline'])['name'].apply(
        ' '.join).reset_index()
    # games = games[["title", "genre_id", "summary", "storyline"]]  # only use these columns
    return games


def pre_process_games(games):
    """ Cleans data and creates a bag-of-words model of the dataset.
            :return A DataFrame matrix with the ordered keywords added. """
    print("Pre-processing data...")
    rake = Rake()
    games['ordered_keywords'] = ""
    columns = games.columns
    for i, row in games.iterrows():
        keywords = ""
        for column in columns:
            if column != 'game_id':  # exclude redundant learning points
                entry = row[column]
                rake.extract_keywords_from_text(entry)
                for word in rake.get_word_degrees().keys():
                    keywords += word + " "

        rake.extract_keywords_from_text(keywords)
        key_words_dict_scores = rake.get_word_degrees()
        ordered_keywords = ""
        for word in key_words_dict_scores.keys():
            ordered_keywords += word + " "

        Game.objects.filter(game_id=row['game_id']).update(ordered_keywords=ordered_keywords)


if __name__ == '__main__':
    print("Starting game data import...")
    clear_database()
    import_file('games_v3.json')
    games = combine_dbs()
    pre_process_games(games)
    print("Import complete!")
