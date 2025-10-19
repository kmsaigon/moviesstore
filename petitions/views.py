from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Petition, Vote
from .forms import PetitionForm

# Create your views here.
def index(request):
    """Display all petitions"""
    petitions = Petition.objects.all()
    template_data = {}
    template_data['title'] = 'Petitions'
    template_data['petitions'] = petitions
    return render(request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create_petition(request):
    """Create a new petition"""
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('petitions.index')
    else:
        form = PetitionForm()
    
    template_data = {}
    template_data['title'] = 'Create Petition'
    template_data['form'] = form
    return render(request, 'petitions/create.html', {'template_data': template_data})

@login_required
def vote_petition(request, petition_id):
    """Vote on a petition (yes/no)"""
    if request.method == 'POST':
        petition = get_object_or_404(Petition, id=petition_id)
        vote_type = request.POST.get('vote_type')
        
        if vote_type not in ['yes', 'no']:
            messages.error(request, 'Invalid vote type.')
            return redirect('petitions.index')
        
        # Get or create vote for this user and petition
        vote, created = Vote.objects.get_or_create(
            petition=petition,
            user=request.user,
            defaults={'vote_type': vote_type}
        )
        
        if not created:
            # User already voted, update their vote
            old_vote_type = vote.vote_type
            vote.vote_type = vote_type
            vote.save()
            
            if old_vote_type != vote_type:
                messages.success(request, f'Your vote has been changed to {vote_type}.')
            else:
                messages.info(request, f'You have already voted {vote_type} on this petition.')
        else:
            messages.success(request, f'Your {vote_type} vote has been recorded!')
        
        # Update petition vote counts
        petition.update_vote_counts()
        
        return redirect('petitions.index')
    
    return redirect('petitions.index')