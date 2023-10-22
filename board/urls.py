from django.urls import path
from django.shortcuts import redirect

from .views import Index, CreatePost, PostItem, EditPost, DeletePost, Responses, Respond, response_accept, \
  response_delete


urlpatterns = [
  path('index', Index.as_view(), name='index'),
  path('post/<int:pk>', PostItem.as_view()),
  path('create_ad', CreatePost.as_view(), name='create_ad'),
  path('post/<int:pk>/edit', EditPost.as_view()),
  path('post/<int:pk>/delete', DeletePost.as_view()),
  path('responses', Responses.as_view(), name='responses'),
  path('responses/<int:pk>', Responses.as_view(), name='responses'),
  path('respond/<int:pk>', Respond.as_view(), name='respond'),
  path('response/accept/<int:pk>', response_accept),
  path('response/delete/<int:pk>', response_delete),
  path('', lambda request: redirect('index', permanent=False)),
]
