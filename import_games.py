import json
import os
from functools import reduce

import django
import pandas
from django.db import connection

from recommender_libraries.lib.rake import Rake

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameplan_project.settings')
django.setup()

from gameplan.models import Game, Genre, GameMode, Franchise, GameEngine, InvolvedCompany, Company, Platform, \
    PlayerPerspective, ReleaseDate, Screenshot, Theme, Video, Website


def clear_database():
    print("Purging all Game entries in database.")
    Game.objects.all().delete()
    Genre.objects.all().delete()
    GameMode.objects.all().delete()
    Franchise.objects.all().delete()
    GameEngine.objects.all().delete()
    InvolvedCompany.objects.all().delete()
    Company.objects.all().delete()
    Platform.objects.all().delete()
    PlayerPerspective.objects.all().delete()
    ReleaseDate.objects.all().delete()
    Screenshot.objects.all().delete()
    Theme.objects.all().delete()
    Video.objects.all().delete()
    Website.objects.all().delete()
    PlayerPerspective.objects.all().delete()

    print("Purge complete.")


def import_file(filename):
    with open(filename, encoding='utf-8') as file:
        data = json.loads(file.read())

        game_data = data['games']
        games = list()
        for i in range(0, len(game_data) - 1):  # len(game_data) - 1
            game = game_data[i]
            print("Adding game: " + game['name'])

            game_object = Game.objects.create(game_id=game['id'], title=game['name'])

            if 'summary' in game:
                game_object.summary = game['summary']

            if 'storyline' in game:
                game_object.storyline = game['storyline']

            if 'cover' in game:
                if not isinstance(game['cover'], int):
                    if 'url' in game['cover']:
                        url = game['cover']['url']
                        url = str(url).strip('/').replace('t_thumb', 't_cover_big')
                        game_object.cover = url

            if 'genres' in game:
                for genre in game['genres']:
                    genre = Genre.objects.get_or_create(genre_id=genre['id'], name=genre['name'])[0]
                    game_object.genres.add(genre)

            if 'category' in game:
                game_object.category = game['category']

            if 'first_release_date' in game:
                game_object.first_release_date = game['first_release_date']

            if 'franchise' in game:
                franchise = \
                    Franchise.objects.get_or_create(franchise_id=game['franchise']['id'],
                                                    name=game['franchise']['name'])[0]
                game_object.franchise = franchise

            if 'game_engines' in game:
                for game_engine in game['game_engines']:
                    if not isinstance(game_engine, int):
                        game_engine = \
                            GameEngine.objects.get_or_create(game_engine_id=game_engine['id'], name=game_engine['name'])[0]
                        game_object.game_engines.add(game_engine)

            if 'game_modes' in game:
                for gamemode in game['game_modes']:
                    gamemode = GameMode.objects.get_or_create(game_mode_id=gamemode['id'], name=gamemode['name'])[0]
                    game_object.game_modes.add(gamemode)

            if 'hypes' in game:
                game_object.hypes = game['hypes']

            if 'involved_companies' in game:
                for involved_company in game['involved_companies']:
                    company = Company.objects.get_or_create(company_id=involved_company['company']['id'],
                                                            name=involved_company['company']['name'])[0]

                    involved_company = InvolvedCompany.objects.get_or_create(involved_company_id=involved_company['id'],
                                                                             developer=involved_company['developer'],
                                                                             publisher=involved_company['publisher'],
                                                                             company=company)[0]
                    game_object.involved_companies.add(involved_company)

            if 'keywords' in game:
                all_keywords = ''
                for keyword in game['keywords']:
                    all_keywords += keyword['name'] + ', '

                game_object.keywords = all_keywords

            if 'platforms' in game:
                for platform in game['platforms']:
                    platform = Platform.objects.get_or_create(platform_id=platform['id'], name=platform['name'])[0]
                    game_object.platforms.add(platform)

            if 'player_perspectives' in game:
                for perspective in game['player_perspectives']:
                    perspective = PlayerPerspective.objects.get_or_create(player_perspective_id=perspective['id'],
                                                                          name=perspective['name'])[0]
                    game_object.player_perspectives.add(perspective)

            if 'popularity' in game:
                game_object.popularity = game['popularity']

            if 'release_dates' in game:
                for date in game['release_dates']:
                    platform = Platform.objects.get_or_create(platform_id=date['platform']['id'],
                                                              name=date['platform']['name'])[0]
                    dateToAdd = ReleaseDate.objects.get_or_create(release_date_id=date['id'], platform=platform)[0]

                    if 'date' in date:
                        dateToAdd.date = date['date']

                    if 'human' in date:
                        dateToAdd.human = date['human']

                    game_object.release_dates.add(dateToAdd)

            if 'screenshots' in game:
                for screenshot in game['screenshots']:
                    url = screenshot['url']
                    url = str(url).strip('/').replace('t_thumb', 't_screenshot_big')

                    screenshot = \
                        Screenshot.objects.get_or_create(screenshot_id=screenshot['id'], url=url)[0]
                    game_object.screenshots.add(screenshot)

            if 'themes' in game:
                for theme in game['themes']:
                    theme = Theme.objects.get_or_create(theme_id=theme['id'], name=theme['name'])[0]
                    game_object.themes.add(theme)

            if 'total_rating' in game:
                game_object.total_rating = game['total_rating']

            if 'total_rating_count' in game:
                game_object.total_rating_count = game['total_rating_count']

            if 'url' in game:
                game_object.url = game['url']

            if 'videos' in game:
                for video in game['videos']:
                    if not isinstance(video, int):
                        video = Video.objects.get_or_create(id=video['id'], video_id=video['video_id'])[0]
                        game_object.videos.add(video)

            if 'websites' in game:
                for website in game['websites']:
                    website = Website.objects.get_or_create(website_id=website['id'], url=website['url'])[0]
                    game_object.websites.add(website)

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
    import_file('games_v4.json')
    games = combine_dbs()
    pre_process_games(games)
    print("Import complete!")
