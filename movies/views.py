from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MovieRequest, Rating
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import MovieRequestForm

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all() 
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie).order_by('-date')

    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(movie=movie, user=request.user)
        except Rating.DoesNotExist:
            pass

    if request.method == 'POST' and 'rating' in request.POST and request.user.is_authenticated:
        rating_value = request.POST.get('rating')
        if rating_value:
            rating, created = Rating.objects.update_or_create(
                movie=movie,
                user=request.user,
                defaults={'rating': rating_value}
            )
            return redirect('movies.show', id=id)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['user_rating'] = user_rating
    template_data['average_rating'] = movie.average_rating()

    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required

def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def requests_view(request):
    if request.method == 'POST':
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            movie_request = form.save(commit=False)
            movie_request.user = request.user
            try:
                movie_request.save()
                messages.success(request, 'Request submitted.')
            except Exception:
                form.add_error('name', 'You have already requested this movie.')
        else:
            # fall through to render with errors
            pass
    else:
        form = MovieRequestForm()

    user_requests = MovieRequest.objects.filter(user=request.user)
    paginator = Paginator(user_requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template_data = {}
    template_data['title'] = 'Requests'
    template_data['form'] = form
    template_data['page_obj'] = page_obj
    return render(request, 'movies/requests.html', {'template_data': template_data})


@login_required
@require_POST
def delete_request(request, pk):
    movie_request = get_object_or_404(MovieRequest, pk=pk, user=request.user)
    movie_request.delete()
    messages.success(request, 'Request deleted.')
    return redirect('movies.requests')
