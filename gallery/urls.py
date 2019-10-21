from django.urls import path
from . import views

app_name = "gallery"

urlpatterns=[
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:id>/update/', views.update, name="update"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:id>/', views.detail, name="detail"),
    path('<int:id>/create/comment', views.create_comment, name="create_comment"),
    path('<int:question_id>/delete/comment/<int:comment_id>', views.delete_comment, name="delete_comment"),
    path('<int:question_id>/update/comment/<int:comment_id>', views.update_comment, name="update_comment"), 

]