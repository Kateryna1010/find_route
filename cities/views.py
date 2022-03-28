from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from cities.forms import CityForm
from cities.models import City


# def home(request, pk=None):
#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         if form.is_valid():
#             form.save()
#     form = CityForm()
#     qs = City.objects.all()
#     lst = Paginator(qs, 5)
#     page_number = request.GET.get('page')
#     page_obj = lst.get_page(page_number)
#     context = {'page_obj': page_obj, 'form': form}
#     return render(request, 'cities/home.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Creating succeed'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Updating succeed'


class CityDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = City
    success_url = reverse_lazy('cities:home')
    success_message = 'Deleting succeed'


class CityListView(ListView):
    model = City
    paginate_by = 5
    template_name = 'cities/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CityForm()
        context['form'] = form
        return context





