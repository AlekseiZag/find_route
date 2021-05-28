from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from cities.models import City
from routes.forms import RouteForm, RouteModelForm

# Create your views here.
from routes.models import Route
from routes.utils import get_routes
from trains.models import Train


# @login_required
def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as e:
                messages.error(request, e)
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})
    else:
        form = RouteForm()
        messages.error(request, "Нет данных для поиска")
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            total_time = int(data['total_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_list = [int(t) for t in trains if t.isdigit()]
            qs = Train.objects.filter(id__in=trains_list).select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()
            form = RouteModelForm(initial={
                'user': data['user'],
                'from_city': cities[from_city_id],
                'to_city': cities[to_city_id],
                'travel_times': total_time,
                'trains': qs,
            })
            context['form'] = form
        return render(request, 'routes/create.html', context)
    else:
        messages.error(request, "Невозможно сохранить несуществующий маршрут")
        return redirect('/')


# @login_required
def save_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            try:
                route.user = request.user
                route.save()
                messages.success(request, "Маршрут успешно сохранен")
                return redirect('/')
            except ValueError:
                messages.error(request, "Необходимо войти или зарегистрироваться")
                return redirect('accounts:login')
        return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, "невозможно сохранить несуществующий маршрут")
        return redirect('/')


class RouteListView(LoginRequiredMixin, ListView):
    model = Route
    # paginate_by = 10
    template_name = 'routes/list.html'
    context_object_name = 'routes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = context['routes'].filter(user=self.request.user)
        return context


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/detail.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удален.')
        return self.post(request, *args, **kwargs)
