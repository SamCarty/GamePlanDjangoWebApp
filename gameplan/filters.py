import django_filters as df
from django import forms

from gameplan.models import Game, Platform, Genre

"""
class PlatformsFilter(df.ModelMultipleChoiceFilter):
    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        for v in values:
            qs = qs.filter(platforms=v)
        return 


class GenresFilter(df.ModelMultipleChoiceFilter):
    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        for v in values:
            qs = qs.filter(genres=v)
        return qs
        """


class GameFilter(df.FilterSet):
    q = df.CharFilter(label='Query', field_name='title', lookup_expr='icontains')
    platforms = df.ModelMultipleChoiceFilter(label='Platform', queryset=Platform.objects.all(), widget=forms.CheckboxSelectMultiple)
    genres = df.ModelMultipleChoiceFilter(label='Genre', queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Game
        fields = ('q', 'platforms', 'genres')



"""
class GameFilter(df.FilterSet):
    q = df.CharFilter(label='Query', field_name='title', lookup_expr='icontains')
    platforms = CustomFilter(label='Platform', queryset=Platform.objects.all(),
                                             widget=forms.CheckboxSelectMultiple, conjoined=False)
    genres = CustomFilter(label='Genre', queryset=Genre.objects.all(),
                                          widget=forms.CheckboxSelectMultiple, conjoined=False)

    class Meta:
        model = Game
        fields = ('q', 'platforms', 'genres')
"""
