from django.urls import path
from pydantic import BaseSettings

from . import views
from refs.apps import RefService


class RefServiceConfig(BaseSettings):
    user_graph_data_path: str

config = RefServiceConfig()
ref_service = RefService(config.user_graph_data_path)


urlpatterns = [
    path(
        "",
        views.UsersInfoView.as_view(ref_service=ref_service),
        name="users_info",
    ),
    path(
        "<str:user_id>",
        views.UserInfoView.as_view(ref_service=ref_service),
        name="user_info",
    ),
]
