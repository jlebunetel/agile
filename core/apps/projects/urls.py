from django.urls import path

from projects.views import (
    ProductDetailView,
    ProductListView,
)

app_name = "projects"

urlpatterns = [
    path("products/<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/", ProductListView.as_view(), name="product-list"),
]
