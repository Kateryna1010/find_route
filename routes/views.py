from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from cities.models import City
from routes.forms import RouteForm, RouteModelForm
from routes.models import Route
from routes.utils import get_routes
from trains.models import Train


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
        messages.error(request, 'No values for search')
        return render(request, 'routes/home.html', {'form': form})

def add_route(request):
    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            travel_time = int(data['travel_time'])
            trains = data['trains'].split(',')
            trains_lst = [int(t) for t in trains if t.isdigit()]
            qs = Train.objects.filter(id__in=trains_lst).select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[to_city_id, from_city_id]).in_bulk()
            form = RouteModelForm(initial={
                'from_city': cities[from_city_id],
                'to_city': cities[to_city_id],
                'travel_time': travel_time,
                'trains': qs
            })
            context['form'] = form
            context['trains'] = qs
        return render(request, 'routes/create.html', context)
    else:
        messages.error(request, 'No routes to save')
        redirect('/')

def save_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route saved successfully')
            return redirect('/')
        return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, 'No routes to save')
        redirect('/')


class RouteListView(ListView):
    model = Route
    paginate_by = 5
    template_name = 'routes/list.html'


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/detail.html'
    context_object_name = 'trains'


class RouteDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('home')
    success_message = 'Deleting succeed'