from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from projects.models import (
    Product,
)
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
