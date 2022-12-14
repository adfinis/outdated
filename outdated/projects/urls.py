from django.urls import path

from . import views
from .views import CreateFormView

urlpatterns = [
    path("", views.index, name="index"),
    path("create", CreateFormView.as_view(), name="create"),
]
