from main.models import UserArtist, UserTagArtist
from main.forms import UserForm, ArtistForm
from django.shortcuts import render, get_list_or_404
from collections import Counter
from main.recommendations import recommend_artists, load_similarities
from main.populate import populate_database
from main.index import load_data
from main.index import search_all_index, search_by_id_index
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
    return render(request, 'index.html')


def home(request): 
    return render(request, 'home.html')


@permission_required('is_superuser')
def scraping(request):
    items = load_data()
    params = {'num_items': len(items), 'items': items}
    return render(request, 'scraping.html', params)


@permission_required('is_superuser')
def search_all(request):
    items = search_all_index()
    params = {'num_items': len(items), 'items': items}
    return render(request, 'search_all.html', params)


@login_required
def catalog(request):
    items = search_all_index()
    params = {'num_items': len(items), 'items': items}
    return render(request, 'catalog.html', params)


@login_required
def product_detail(request, id):
    item = search_by_id_index(id)
    params = {'item': item}
    return render(request, 'product_detail.html', params)


@login_required
def profile(request):
    return render(request, 'profile.html')


def populateDB(request):
    populate_database() 
    return render(request, 'populate.html')

def loadRS(request):
    load_similarities()
    return render(request,'loadRS.html')

def mostListenedArtists(request):
    form = UserForm(request.GET, request.FILES)
    if form.is_valid():
        user = form.cleaned_data['id'] 
        user_artists = UserArtist.objects.filter(user=user).order_by('-listen_time')[:5]
        params = {'form': form, 'user_artists': user_artists}
    else:
        params = {'form': UserForm()}
    return render(request,'mostListenedArtists.html', params)

def mostFrequentTags(request):
    form = ArtistForm(request.GET, request.FILES)
    if form.is_valid():
        artist = form.cleaned_data['id']
        tags = [
            elem.tag.value
            for elem in get_list_or_404(UserTagArtist, artist=artist)
        ]
        params = {'form': form, 'tags': Counter(tags).most_common(10)}
    else:
        params = {'form': ArtistForm()}
    return render(request,'mostFrequentTags.html', params)

def recommendedArtists(request):
    form = UserForm(request.GET, request.FILES)
    if form.is_valid():
        user = form.cleaned_data['id']
        artists = recommend_artists(int(user))
        params = {'form': form, 'artists': artists}
    else:
        params = {'form': UserForm()}
    return render(request,'recommendedArtists.html', params)

def styles(request): 
    return render(request,'styles.html')