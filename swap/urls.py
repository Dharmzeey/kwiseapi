from django.urls import path

from .views import (
    DefectListView,
    EstimateView,
    ModelListView,
    SeriesListView,
    StorageListView,
)

urlpatterns = [
    path("series/",                 SeriesListView.as_view(),  name="swap-series"),
    path("models/<int:series_id>/", ModelListView.as_view(),   name="swap-models"),
    path("storage/<int:model_id>/", StorageListView.as_view(), name="swap-storage"),
    path("defects/",                DefectListView.as_view(),  name="swap-defects"),
    path("estimate/",               EstimateView.as_view(),    name="swap-estimate"),
]
