from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("modules/", views.module_list, name="module-list"),
    path("modules/<str:module_id>/", views.module_detail, name="module-detail"),
]
