from django.urls import path
from . import views

app_name = "Addnotes" 

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("notes", views.notes, name="notes"),
    path('del/<str:item_id>', views.remove, name="del"),
    # path('notes/<int:pk>/delete/', views.delete_note, name='delete_single_note')
]