import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from refs.service import RefService
from refs.entities import User


class UserInfoView(View):
    ref_service: RefService = None

    def __init__(self, ref_service: RefService):
        self._ref_service = ref_service

    def get(self, request, user_id: str):
        user = self._ref_service.get_user(user_id)

        data = todict(user)

        return HttpResponse(json.dumps(data), content_type='application/json')


def todict(user: User) -> dict:
    return {
        "pk": user.pk,
        "ref_level": user.ref_level.value,
        "team_size": user.team_size,
        "balance": user.balance,
        "refs": [pk for pk in user.ref_pks],
    }
