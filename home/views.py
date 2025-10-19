from django.shortcuts import render
from django.db.models import Sum, Count
from django.conf import settings
from accounts.models import UserProfile
from cart.models import Item
from movies.models import Movie

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html',
                  {'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html',
                  {'template_data': template_data})

def map(request):
    template_data = {}
    template_data['title'] = 'Local Popularity Map'
    
    # Get trending movies by state
    # Aggregate purchase data: Item -> Order -> User -> UserProfile -> location
    state_trending = {}
    
    # Get all states that have purchases
    states_with_purchases = UserProfile.objects.filter(
        user__order__item__isnull=False,
        location__isnull=False
    ).values_list('location', flat=True).distinct()
    
    for state in states_with_purchases:
        # Get all items purchased by users in this state
        items_in_state = Item.objects.filter(
            order__user__userprofile__location=state
        ).select_related('movie')
        
        # Calculate total quantity per movie
        movie_totals = {}
        for item in items_in_state:
            movie_id = item.movie.id
            if movie_id not in movie_totals:
                movie_totals[movie_id] = {
                    'movie': item.movie,
                    'total_quantity': 0,
                    'total_orders': 0
                }
            movie_totals[movie_id]['total_quantity'] += item.quantity
            movie_totals[movie_id]['total_orders'] += 1
        
            # Sort by total quantity and get top 5
            trending_movies = sorted(
                    movie_totals.values(),
                    key=lambda x: x['total_quantity'],
                    reverse=True
                )[:5]

            # Convert Django Movie objects to simple dictionaries for JavaScript
            trending_movies_data = []
            for movie_data in trending_movies:
                trending_movies_data.append({
                    'movie_id': movie_data['movie'].id,
                    'movie_title': movie_data['movie'].name,  # Changed from .title to .name
                    'movie_image': movie_data['movie'].image.url if movie_data['movie'].image else '',
                    'total_quantity': movie_data['total_quantity'],
                    'total_orders': movie_data['total_orders']
                })

            state_trending[state] = trending_movies_data
    
    # US state coordinates for map markers (simplified - just center points)
    state_coordinates = {
        'AL': {'lat': 32.806671, 'lng': -86.791130, 'name': 'Alabama'},
        'AK': {'lat': 61.370716, 'lng': -152.404419, 'name': 'Alaska'},
        'AZ': {'lat': 33.729759, 'lng': -111.431221, 'name': 'Arizona'},
        'AR': {'lat': 34.969704, 'lng': -92.373123, 'name': 'Arkansas'},
        'CA': {'lat': 36.116203, 'lng': -119.681564, 'name': 'California'},
        'CO': {'lat': 39.059811, 'lng': -105.311104, 'name': 'Colorado'},
        'CT': {'lat': 41.597782, 'lng': -72.755371, 'name': 'Connecticut'},
        'DE': {'lat': 39.318523, 'lng': -75.507141, 'name': 'Delaware'},
        'FL': {'lat': 27.766279, 'lng': -82.640371, 'name': 'Florida'},
        'GA': {'lat': 33.040619, 'lng': -83.643074, 'name': 'Georgia'},
        'HI': {'lat': 21.094318, 'lng': -157.498337, 'name': 'Hawaii'},
        'ID': {'lat': 44.240459, 'lng': -114.478828, 'name': 'Idaho'},
        'IL': {'lat': 40.349457, 'lng': -88.986137, 'name': 'Illinois'},
        'IN': {'lat': 39.849426, 'lng': -86.258278, 'name': 'Indiana'},
        'IA': {'lat': 42.011539, 'lng': -93.210526, 'name': 'Iowa'},
        'KS': {'lat': 38.526600, 'lng': -96.726486, 'name': 'Kansas'},
        'KY': {'lat': 37.668140, 'lng': -84.670067, 'name': 'Kentucky'},
        'LA': {'lat': 31.169546, 'lng': -91.867805, 'name': 'Louisiana'},
        'ME': {'lat': 44.323535, 'lng': -69.765261, 'name': 'Maine'},
        'MD': {'lat': 39.063946, 'lng': -76.802101, 'name': 'Maryland'},
        'MA': {'lat': 42.230171, 'lng': -71.530106, 'name': 'Massachusetts'},
        'MI': {'lat': 43.326618, 'lng': -84.536095, 'name': 'Michigan'},
        'MN': {'lat': 45.694454, 'lng': -93.900192, 'name': 'Minnesota'},
        'MS': {'lat': 32.741646, 'lng': -89.678696, 'name': 'Mississippi'},
        'MO': {'lat': 38.572954, 'lng': -92.189283, 'name': 'Missouri'},
        'MT': {'lat': 47.052952, 'lng': -110.454353, 'name': 'Montana'},
        'NE': {'lat': 41.125370, 'lng': -98.268082, 'name': 'Nebraska'},
        'NV': {'lat': 38.313515, 'lng': -117.055374, 'name': 'Nevada'},
        'NH': {'lat': 43.452492, 'lng': -71.563896, 'name': 'New Hampshire'},
        'NJ': {'lat': 40.298904, 'lng': -74.521011, 'name': 'New Jersey'},
        'NM': {'lat': 34.840515, 'lng': -106.248482, 'name': 'New Mexico'},
        'NY': {'lat': 42.165726, 'lng': -74.948051, 'name': 'New York'},
        'NC': {'lat': 35.630066, 'lng': -79.806419, 'name': 'North Carolina'},
        'ND': {'lat': 47.528912, 'lng': -99.784012, 'name': 'North Dakota'},
        'OH': {'lat': 40.388783, 'lng': -82.764915, 'name': 'Ohio'},
        'OK': {'lat': 35.565342, 'lng': -96.928917, 'name': 'Oklahoma'},
        'OR': {'lat': 44.572021, 'lng': -122.070938, 'name': 'Oregon'},
        'PA': {'lat': 40.590752, 'lng': -77.209755, 'name': 'Pennsylvania'},
        'RI': {'lat': 41.680893, 'lng': -71.511780, 'name': 'Rhode Island'},
        'SC': {'lat': 33.856892, 'lng': -80.945007, 'name': 'South Carolina'},
        'SD': {'lat': 44.299782, 'lng': -99.438828, 'name': 'South Dakota'},
        'TN': {'lat': 35.747845, 'lng': -86.692345, 'name': 'Tennessee'},
        'TX': {'lat': 31.968599, 'lng': -99.901813, 'name': 'Texas'},
        'UT': {'lat': 40.150032, 'lng': -111.862434, 'name': 'Utah'},
        'VT': {'lat': 44.045876, 'lng': -72.710686, 'name': 'Vermont'},
        'VA': {'lat': 37.769337, 'lng': -78.169968, 'name': 'Virginia'},
        'WA': {'lat': 47.400902, 'lng': -121.490494, 'name': 'Washington'},
        'WV': {'lat': 38.491226, 'lng': -80.954453, 'name': 'West Virginia'},
        'WI': {'lat': 44.268543, 'lng': -89.616508, 'name': 'Wisconsin'},
        'WY': {'lat': 42.755966, 'lng': -110.454353, 'name': 'Wyoming'},
    }
    
    template_data['state_trending'] = state_trending
    template_data['state_coordinates'] = state_coordinates
    template_data['states_with_purchases'] = list(states_with_purchases)
    template_data['GOOGLE_MAPS_API_KEY'] = settings.GOOGLE_MAPS_API_KEY
    
    return render(request, 'home/map.html', {'template_data': template_data})