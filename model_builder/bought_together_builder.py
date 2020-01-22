import os
from collections import defaultdict

import pytz
from django.utils.datetime_safe import datetime
from itertools import combinations

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameplan_project.settings')
django.setup()

from gameplan.models import Game
from gatherer.models import Log
from recommender.models import RecommendationPairing


def clear_db():
    RecommendationPairing.objects.all().delete()


def get_buy_events():
    """ Gets all the 'purchase_event' events. """
    events = Log.objects.filter(event_type='purchase_event').values()
    return events


def collate_transactions(purchases):
    """ Creates a dictionary of lists containing the content ids from each session.
     :returns Dictionary of Lists. """
    trans = defaultdict(list)

    for item in purchases:
        session = item['session_id']
        trans[session].append(item['content_id'])

    return trans


def bought_together(session_trans, min=0.01):
    """ Calculates the item pairings and pairing rules for each session transaction.
    :returns a sorted list of bought together rules. """
    n = len(session_trans)
    one_sets = get_cumulative_items(session_trans, min)
    print(one_sets)
    two_sets = get_item_pairings(session_trans, one_sets)
    print(two_sets)

    rules = get_bought_together_rules(one_sets, two_sets, n)
    return sorted(rules)


def get_cumulative_items(session_trans, min):
    """ Generates a dictionary of item sets that show the frequency of item purchases per session.
     :returns Dictionary of FrozenSets - one for each item. """
    n = len(session_trans)
    temp = defaultdict(int)
    cumulative_set = dict()

    for key, items in session_trans.items():
        for item in items:
            index = frozenset({item})  # frozenset because values are immutable and can be used as dict key.
            temp[index] += 1

    for key, set in temp.items():
        if set > min * n:
            cumulative_set[key] = set

    return cumulative_set


def get_item_pairings(session_trans, one_sets):
    """ Generates a dictionary of item sets that show the frequency of two items purchased in the same session
     as each other.
     :returns Dictionary of FrozenSets - one for each permutation of possible combinations. """
    item_pairings = defaultdict(int)

    for key, items in session_trans.items():
        items = list(set(items))

        if len(items) > 2:
            for permutation in combinations(items, 2):
                if permutation_in_cumulative_set(permutation, one_sets):
                    item_pairings[frozenset(permutation)] += 1
        elif len(items) == 2:
            if permutation_in_cumulative_set(items, one_sets):
                item_pairings[frozenset(items)] += 1

    return item_pairings


def permutation_in_cumulative_set(permutation, cumulative_set):
    """ Checks if the permutation provided is in the cumulative set.
     :returns Boolean true if both values are in the set. """
    return frozenset({permutation[0]}) in cumulative_set and frozenset({permutation[1]}) in cumulative_set


def get_bought_together_rules(one_sets, two_sets, n):
    """ Create the list of all bought together item pairings with confidence and support values.
     :returns List of 'bought together' item rules. """
    rules = list()
    for from_game, cumulative_freq in one_sets.items():  # game id, number of times purchased
        for game_pairings, pairing_freq in two_sets.items():  # game ids (pairings), number of times paired together
            # if the game is paired with us, keep going... (if not, we don't care about it!)
            if from_game.issubset(game_pairings):
                target = game_pairings.difference(from_game)  # extract the 'to_game' id by finding the difference.

                # support is the percentage of sessions that contain both items
                # - support(x -> y) = (x ^ y) / (total transactions)
                support = pairing_freq / n
                # confidence is the trust we have in finding item B given item A - confidence(x -> y) = (x ^ y) / (x)
                confidence = pairing_freq / cumulative_freq

                # next(iter()) because we need the value, not the frozenset
                rules.append((next(iter(from_game)), next(iter(target)), confidence, support))

    return rules


def save_results(results):
    for i in range(0, len(results) - 1):
        item = results[i]
        created = datetime.now(pytz.utc)
        from_game = Game.objects.get(game_id=item[0])
        to_game = Game.objects.get(game_id=item[1])

        rec_object = RecommendationPairing.objects.create(created=created, from_game=from_game, to_game=to_game,
                                                          confidence=item[2], support=item[3], )
        rec_object.save()


if __name__ == '__main__':
    clear_db()
    e = get_buy_events()
    t = collate_transactions(e)
    bought_together = bought_together(t)
    save_results(bought_together)

