from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, NoteViewSet, CommentViewSet, LikeViewSet
from . import views


# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'notes', NoteViewSet)
# router.register(r'comments', CommentViewSet)
# router.register(r'likes', LikeViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path('api/', include(router.urls))
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('add_note', views.add_note, name='add_note'),
    path('get_user_notes', views.get_user_notes, name='get_user_notes'),
    path('update_note/<int:note_id>', views.update_note, name='update_note'),
    path('delete_note/<int:note_id>', views.delete_note, name='delete_note'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('check_auth_status', views.check_auth_status, name='check_auth_status'),


]
