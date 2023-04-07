from django.urls import path
from pydantic import BaseSettings, Field

from . import views
from refs.service import RefService


class RefServiceConfig(BaseSettings):
    user_graph_data_path: str = Field("./../data/data.json")


config = RefServiceConfig()
ref_service = RefService()


urlpatterns = [
    path(
        "<str:user_id>",
        views.UserInfoView.as_view(ref_service=ref_service),
        name="user_info",
    ),
]
