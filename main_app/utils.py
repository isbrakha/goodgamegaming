import re, json
from datetime import datetime
from .models import Game

def sanitize_platform_data(platform_data):
    sanitized_data = re.sub(r"'(?![^<]*>)", '"', platform_data)
    finalized_sanitized_data = re.sub(r'class="([^"]*)"', r'class=\'$1\'', sanitized_data)
    return finalized_sanitized_data


def save_game_to_database(game_data):
    genre_names = [genre['name'] for genre in game_data.get('genres', [])]
    game_platforms = game_data.get('platforms', [])
    fixed_platform_data = sanitize_platform_data(str(game_platforms)).replace("None", "null")
    platform_data = json.loads(fixed_platform_data)
    platform_names = [platform['platform']['name'] for platform in platform_data]

    print(platform_names)
    defaults = { 
        'name': game_data.get('name', ''),
        'rating': game_data.get('rating', 0.0),
        'released': datetime.strptime(game_data.get('released', ''), '%Y-%m-%d').date() if game_data.get('released') else None,
        'image': game_data.get('background_image', ''),
        'platforms': platform_names,
        'developer': game_data.get('developer', ''),
        'publisher': game_data.get('publisher', ''),
        'description': game_data.get('description', ''),
        'esrb_rating': game_data.get('esrb_rating', ''),
        'genres': genre_names
    }
    
    game, created = Game.objects.get_or_create(id=game_data.get('id', 0), defaults=defaults)
    if not created:
        for field, value in defaults.items():
            setattr(game, field, value)
        game.save()

