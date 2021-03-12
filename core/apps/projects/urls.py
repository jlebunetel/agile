from django.urls import path
from projects.views import (
    ProductDetailView,
    ProductListView,
    SprintDetailView,
    SprintListView,
)

app_name = "projects"

urlpatterns = []


urlpatterns = [
    path("products/<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("sprints/<int:pk>/", SprintDetailView.as_view(), name="sprint-detail"),
    path("sprints/", SprintListView.as_view(), name="sprint-list"),
]
