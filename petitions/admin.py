# Import Django's admin module for configuring the admin interface
from django.contrib import admin
# Import our custom models
from .models import Petition, Vote

# Register your models here.

@admin.register(Petition)  # Decorator that registers the Petition model with the admin interface
class PetitionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Petition model.
    This defines how petitions are displayed and managed in the Django admin interface.
    """
    
    # Fields to display in the admin list view
    # This makes it easy to see key information about petitions at a glance
    list_display = ['movie_title', 'genre', 'created_by', 'created_date', 'yes_votes', 'no_votes', 'total_votes']
    
    # Filter options in the admin sidebar
    # Allows admins to filter petitions by genre, date, or creator
    list_filter = ['genre', 'created_date', 'created_by']
    
    # Search functionality on these fields
    # Admins can search for petitions by title, description, or genre
    search_fields = ['movie_title', 'description', 'genre']
    
    # Fields that are read-only in the admin form
    # These fields are automatically calculated or set, so they shouldn't be editable
    readonly_fields = ['created_date', 'yes_votes', 'no_votes', 'total_votes']
    
    # Default ordering for the admin list view
    # Shows newest petitions first
    ordering = ['-created_date']

@admin.register(Vote)  # Decorator that registers the Vote model with the admin interface
class VoteAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Vote model.
    This defines how votes are displayed and managed in the Django admin interface.
    """
    
    # Fields to display in the admin list view
    # Shows user, petition, vote type, and creation date
    list_display = ['user', 'petition', 'vote_type', 'created_at']
    
    # Filter options in the admin sidebar
    # Allows filtering by vote type and creation date
    list_filter = ['vote_type', 'created_at']
    
    # Search functionality on these fields
    # Uses double underscore notation to search related fields
    # user__username searches the username field of the related User model
    # petition__movie_title searches the movie_title field of the related Petition model
    search_fields = ['user__username', 'petition__movie_title']
    
    # Fields that are read-only in the admin form
    # Timestamps are automatically set, so they shouldn't be editable
    readonly_fields = ['created_at', 'updated_at']
    
    # Default ordering for the admin list view
    # Shows newest votes first
    ordering = ['-created_at']