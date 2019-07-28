from django.urls import path
from . import views

urlpatterns = [
        path('Movie/',views.Movies),
        path('AddMovie/',views.AddMovie),
        path('AddActor/',views.AddActor),
        path('EditMovie/',views.EditMovie),
        path('actormessage/',views.actormessage),
        path('moviemessage/',views.moviemessage),
        path('editmessage/',views.editmessage),
        path('search/',views.search)
]