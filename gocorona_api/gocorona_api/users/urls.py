from django.urls import path

#from rest_framework.urlpatterns import format_suffix_patterns

from gocorona_api.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    CoronaAppList,
    CoronaAppDetail,
    CoronaAppResult,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    path('<str:username>/geo/', CoronaAppList.as_view()),
    path('<str:username>/geo/<int:pk>/', CoronaAppDetail.as_view()),
    path('<str:username>/geo/result/', CoronaAppResult.as_view()),
]
