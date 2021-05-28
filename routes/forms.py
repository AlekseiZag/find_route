from django import forms

from cities.models import City
from routes.models import Route
from trains.models import Train


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control js-example-basic-single',

    }))

    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control js-example-basic-single',

    }))

    cities = forms.ModelMultipleChoiceField(
        label='Через города', queryset=City.objects.all(),
        required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control js-example-basic-multiple'}
        )
    )
    travelling_time = forms.IntegerField(label='Время в пути (в часах)', widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите время в пути',
    }))


class RouteModelForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(label='Названи маршрута', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите название маршрута',
    }))
    from_city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.HiddenInput())

    to_city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.HiddenInput())

    trains = forms.ModelMultipleChoiceField(queryset=Train.objects.all(),
                                            required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control d-none'}

        )
                                            )

    travel_times = forms.IntegerField(label='Время в пути (в часах)', widget=forms.HiddenInput())

    class Meta:
        model = Route
        # fields = '__all__'
        exclude = ('user',)