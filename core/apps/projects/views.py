from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from projects.models import Product, Sprint


class ProductDetailView(DetailView):
    model = Product


class ProductListView(ListView):
    model = Product


class SprintDetailView(DetailView):
    model = Sprint


class SprintListView(ListView):
    model = Sprint
