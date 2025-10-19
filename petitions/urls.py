# Import Django's path function for creating URL patterns
from django.urls import path
# Import the views module from the current app
from . import views

# Define the URL patterns for the petitions app
urlpatterns = [
    # Maps the root URL ('') to the index view
    # This creates the URL /petitions/ and names it 'petitions.index'
    path('', views.index, name='petitions.index'),
    
    # Maps 'create/' to the create_petition view
    # This creates the URL /petitions/create/ and names it 'petitions.create'
    path('create/', views.create_petition, name='petitions.create'),
    
    # Maps '<int:petition_id>/vote/' to the vote_petition view
    # The <int:petition_id> captures an integer parameter from the URL
    # This creates URLs like /petitions/1/vote/, /petitions/2/vote/, etc.
    # The petition_id parameter is passed to the view function
    path('<int:petition_id>/vote/', views.vote_petition, name='petitions.vote'),
]
