from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.home, name='home'),
      path('accounts/signup/', views.signup, name='signup'),
      path('games/', views.games_index, name='games_index'),
      path('add_to_liked', views.add_to_liked, name='add_game'),
      path('games/<int:game_id>/', views.game_detail, name='game_detail'),
      path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
      path('delete_tip/<int:tip_id>/', views.delete_tip, name='delete_tip'),
      path('update-tip/<int:tip_id>/', views.update_tip, name='update_tip'),
]