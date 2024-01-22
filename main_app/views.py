from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from .models import Game, Review, Tip
from .forms import ReviewForm, TipForm
from datetime import datetime
import json, requests, re
from .utils import save_game_to_database
from django.core.paginator import Paginator


def home(request):
  return redirect('games_index')

def signup(request):
  error_message = ''
  if request.method == 'POST':
 
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = """Invalid sign up:
      Username in use or incorrect password.
      Your password can't be entirely numeric.
      our password must contain at least 8 characters."""
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def games_index(request):
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = request.GET.get('page', 1)  # Get the page number from AJAX request
        url = f'https://api.rawg.io/api/games?key=b714af7bd53b4d389217d6baab2bbdad&page={page}&page_size=30'
        response = requests.get(url)
        data = response.json()
        return JsonResponse(data)  # Send JSON response back to AJAX request

   
    url = 'https://api.rawg.io/api/games?key=b714af7bd53b4d389217d6baab2bbdad&page=1&page_size=30'
    response = requests.get(url)
    data = response.json()
    games = data["results"]
    for game in games:
        genre_names = []
        for genre in game['genres']:
            genre_names.append(genre['name'])

        game['genre_names'] = genre_names

    return render(request, 'games/index.html', {'games': games})


@login_required
def add_to_liked(request):
    if request.method == 'POST':
        try:
            game_data = json.loads(request.POST.get('game_data'))
            Game.objects.get_or_create(
                id=game_data['id'],
                name=game_data['name'],
                rating=game_data['rating'],
                released=datetime.strptime(game_data['released'], '%Y-%m-%d').date() if game_data['released'] else None,
                image=game_data['image'],
                platforms=game_data['platforms'],
                developer=game_data['developer'],
                publisher=game_data['publisher'],
                description=game_data['description'],
                esrb_rating=game_data['esrb_rating'],
                genres=game_data['genres'],
                # user=request.user
                
            )

            user = request.user
            print('userprint',user.add_to_liked)


            

            return JsonResponse({'success': 'Game added successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    

def game_detail(request, game_id):
    url = f'https://api.rawg.io/api/games/{game_id}?key=b714af7bd53b4d389217d6baab2bbdad'
    response = requests.get(url)
    game_data = response.json()

    # Save game data to the database
    save_game_to_database(game_data)

    # Try to get the game from your database
    game = Game.objects.get(id=game_id)
    # Fetch reviews and tips from  database
    reviews = Review.objects.filter(game=game)
    tips = Tip.objects.filter(game=game)

    form = ReviewForm(request.POST or None)
    tip_form = TipForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.game = game
            new_review.author = request.user
            new_review.game.user = request.user
            new_review.save()

            # Associate the game with the current user if not already associated
            if game.user != request.user:
                game.user = request.user
                game.save()

        elif tip_form.is_valid():
            new_tip = tip_form.save(commit=False)
            new_tip.game = game
            new_tip.author = request.user
            new_tip.game.user = request.user
            new_tip.save()

            if game.user != request.user:
                game.user = request.user
                game.save()

            return redirect('game_detail', game_id=game_id)
    else:
        form = ReviewForm()
        tip_form = TipForm()

    context = {
        'game': game,
        'reviews': reviews,
        'tips': tips,
        'form': form,
        'tip_form': tip_form
    }


    return render(request, 'games/detail.html', context)

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect(request.META.get('HTTP_REFERER', 'fallback_view_name'))

def delete_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    tip.delete()
    return redirect(request.META.get('HTTP_REFERER', 'fallback_view_name'))


def update_tip(request, tip_id):
    if request.method == 'POST':
        # Get the tip object to update
        tip = get_object_or_404(Tip, pk=tip_id)

        # Update the content based on the POST data
        new_content = request.POST.get('content')
        tip.content = new_content
        tip.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'})