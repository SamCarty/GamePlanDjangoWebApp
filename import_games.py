import json
import os
import string
from functools import reduce
from nltk import WordNetLemmatizer

import django
import pandas
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameplan_project.settings')
django.setup()

from gameplan.models import Game, Genre, GameMode, Franchise, GameEngine, InvolvedCompany, Company, Platform, \
    PlayerPerspective, ReleaseDate, Screenshot, Theme, Video, Website


def clear_database():
    print("[IMPORT] Purging all entries in database.")
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

    print("[IMPORT] Purge complete.")


def import_file(filename, n):
    with open(filename, encoding='utf-8') as file:
        data = json.loads(file.read())

        game_data = data['games']
        games = list()
        for i in range(0, len(game_data) - 1):
            if n == -1 or i < n:
                if len(Game.objects.filter(game_id=game_data[i]['id'])) == 0:
                    game = game_data[i]
                    print("[IMPORT] Adding game: " + game['name'])

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
                            date_to_add = ReleaseDate.objects.get_or_create(release_date_id=date['id'], platform=platform)[0]

                            if 'date' in date:
                                date_to_add.date = date['date']

                            if 'human' in date:
                                date_to_add.human = date['human']

                            game_object.release_dates.add(date_to_add)

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

        print("[IMPORT] " +  str(len(games)) + " items added to database.")
        return games


def combine_dbs():
    """ Imports the dataset and returns the resulting DataFrame matrix. """
    print("[IMPORT] Combining databases...")
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

    return games


def pre_process_games(games):
    """ Cleans data and creates a bag-of-words model of the dataset.
            :return A DataFrame matrix with the ordered keywords added. """

    stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an',
     'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been',
     'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't",
     'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't",
     'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from',
     'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't",
     'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's",
     'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd",
     "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's",
     'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my',
     'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
     'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
     'same', "shan't", 'she', "she'd", "she'll", "she's", 'should',
     "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the',
     'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's",
     'these', 'they', "they'd", "they'll", "they're", "they've", 'this',
     'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was',
     "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't",
     'what', "what's", 'when', "when's", 'where', "where's", 'which',
     'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't",
     'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've",
     'your', 'yours', 'yourself', 'yourselves', 'ios', 'reimagined', 'remastered',
     'redesigned', 'remake', 'xbox', 'pc', 'windows', 'version', 'original', 'game',
     'update', 'playstation', 'ps4']

    print("[IMPORT] Pre-processing data...")
    games['ordered_keywords'] = ""
    columns = games.columns
    for i, row in games.iterrows():
        keywords = ""
        for column in columns:
            if column != 'game_id':  # exclude redundant learning points
                entry = row[column]
                words = entry.split()
                for word in words:
                    word = word.lower()
                    if word not in stopwords:
                        word = ''.join(char for char in word if not char in string.punctuation)
                        lemmatizer = WordNetLemmatizer()
                        word = lemmatizer.lemmatize(word)
                        keywords += word + ' '

        Game.objects.filter(game_id=row['game_id']).update(ordered_keywords=keywords)


if __name__ == '__main__':
    print("[IMPORT] Starting game data import...")
    i = input("Press [1] to reimport the entire database (purge). \nPress [2] to just remake the ordered keywords.")
    if i == '1':
        clear_database()
        import_file('games.json', -1)
    games = combine_dbs()
    pre_process_games(games)
    print("[IMPORT] Import complete!")


def import_max_range(n):
    import_file('games.json', n)
    games = combine_dbs()
    pre_process_games(games)
    print("[IMPORT] Import complete!")
