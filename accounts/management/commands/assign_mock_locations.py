from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, US_STATES
import random

class Command(BaseCommand):
    help = 'Assign random US states to existing users without profiles for demo purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing profiles with new random locations',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        if force:
            # Update all existing profiles with new random locations
            profiles = UserProfile.objects.all()
            updated_count = 0
            for profile in profiles:
                profile.location = random.choice(US_STATES)[0]
                profile.save()
                updated_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Updated {updated_count} existing profiles with random locations')
            )
        else:
            # Only create profiles for users who don't have them
            users_without_profiles = User.objects.filter(userprofile__isnull=True)
            created_count = 0
            
            for user in users_without_profiles:
                random_state = random.choice(US_STATES)[0]
                UserProfile.objects.create(user=user, location=random_state)
                created_count += 1
                self.stdout.write(f'Created profile for {user.username} with location: {random_state}')
            
            self.stdout.write(
                self.style.SUCCESS(f'Created {created_count} new profiles with random locations')
            )
            
            if created_count == 0:
                self.stdout.write(
                    self.style.WARNING('No users found without profiles. Use --force to update existing profiles.')
                )
