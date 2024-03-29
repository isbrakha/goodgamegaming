from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from .models import Game, Review, Tip, UserProfile
from .forms import ReviewForm, TipForm
from datetime import datetime
import json, requests, re
from .utils import save_game_to_database
from django.core.paginator import Paginator
from .models import UserProfile


def home(request):
  return redirect('games_index')

def signup(request):
  error_message = ''
  if request.method == 'POST':
 
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      UserProfile.objects.create(user=user)
      login(request, user)
      return redirect('home')
    else:
      error_message = """Invalid sign up:
      Username in use or incorrect password.
      Your password can't be entirely numeric.
      our password must contain at least 8 characters."""
 
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def games_index(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        liked_game_ids = user_profile.liked_games.values_list('id', flat=True)
    else: 
        liked_game_ids = False
    page = int(request.GET.get('page',1))    
    url = f'https://api.rawg.io/api/games?key=b714af7bd53b4d389217d6baab2bbdad&page={page}&page_size=30'
    response = requests.get(url)
    data = response.json()
    games = data["results"]
    for game in games:
        genre_names = []
        for genre in game['genres']:
            genre_names.append(genre['name'])

        game['genre_names'] = genre_names


 
    return render(request, 'games/index.html', {'games': games, 'liked_game_ids': liked_game_ids, 'page': page})


@login_required
def add_to_liked(request):
    if request.method == 'POST':
        try:
            game_data = json.loads(request.POST.get('game_data'))
            game_id = game_data.get('id')
            print(game_id)
            if not game_id:
                return JsonResponse({'error': 'Game ID is missing'}, status=400)

            released_date = None
            if game_data.get('released'):
                released_date = datetime.strptime(game_data['released'], '%Y-%m-%d').date()

            game, created = Game.objects.get_or_create(
                id=game_id,
                defaults={
                    'name': game_data.get('name', ''),
                    'rating': game_data.get('rating', 0.0),
                    'released': released_date,
                    'image': game_data.get('image', ''),
                    'platforms': game_data.get('platforms', []),
                    'developer': game_data.get('developer', ''),
                    'publisher': game_data.get('publisher', ''),
                    'description': game_data.get('description', ''),
                    'esrb_rating': game_data.get('esrb_rating', ''),
                    'genres': game_data.get('genres', []),
                }
            )

            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.liked_games.add(game)

            return JsonResponse({'success': 'Game added successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def game_detail(request, game_id):
    url = f'https://api.rawg.io/api/games/{game_id}?key=b714af7bd53b4d389217d6baab2bbdad'
    response = requests.get(url)
    game_data = response.json()

    save_game_to_database(game_data)

    game = Game.objects.get(id=game_id)
    # fetch reviews and tips from  database
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

            # assocaite game with user
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
        tip = get_object_or_404(Tip, pk=tip_id)

        new_content = request.POST.get('content')
        tip.content = new_content
        tip.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'})