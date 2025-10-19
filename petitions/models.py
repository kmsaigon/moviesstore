from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    movie_title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    why_add_movie = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    yes_votes = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['created_date'], name='petition_created_idx'),
        ]

    def __str__(self):
        return f"{self.movie_title} by {self.created_by.username}"

    def update_vote_counts(self):
        """Update vote counts based on Vote model"""
        votes = self.vote_set.all()
        self.yes_votes = votes.filter(vote_type='yes').count()
        self.no_votes = votes.filter(vote_type='no').count()
        self.total_votes = votes.count()
        self.save()

class Vote(models.Model):
    VOTE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=3, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['petition', 'user']
        indexes = [
            models.Index(fields=['petition', 'user'], name='vote_petition_user_idx'),
        ]

    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} on {self.petition.movie_title}"