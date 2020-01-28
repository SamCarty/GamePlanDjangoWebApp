import django_filters as df
from django import forms

from gameplan.models import Game, Platform, Genre


class GameFilter(df.FilterSet):
    q = df.CharFilter(label='Query', field_name='title', lookup_expr='icontains')
    platforms = df.ModelMultipleChoiceFilter(label='Platform', queryset=Platform.objects.all().order_by('name'),
                                             widget=forms.CheckboxSelectMultiple, conjoined=True)
    genres = df.ModelMultipleChoiceFilter(label='Genre', queryset=Genre.objects.all().order_by('name'),
                                          widget=forms.CheckboxSelectMultiple, conjoined=True)

    class Meta:
        model = Game
        fields = ('q', 'platforms', 'genres')
