from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from trains.forms import TrainForm
from trains.models import Train


def home(request, pk=None):
    qs = Train.objects.all()
    lst = Paginator(qs, 5)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj, }
    return render(request, 'trains/home.html', context)


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Creating succeed'


class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Updating succeed'


class TrainDeleteView(SuccessMessageMixin, DeleteView):
    model = Train
    success_url = reverse_lazy('trains:home')
    success_message = 'Deleting succeed'


class TrainListView(ListView):
    model = Train
    paginate_by = 5
    template_name = 'trains/home.html'







