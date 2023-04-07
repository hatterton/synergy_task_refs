from typing import List

from refs.models import UserModel
from refs.entities import (
    RefLevel,
    User,
)


def convert_from_models_to_entities(models: List[UserModel]) -> List[User]:
    users = [
        convert_model_to_entity(model)
        for model in models
    ]

    pk2user = {user.pk: user for user in users}

    for model in models:
        if model.parent is None:
            continue

        user = pk2user[model.id]
        parent_user = pk2user.get(model.parent.id)

        if parent_user is not None:
            parent_user.refs.append(user)

    return users


def convert_from_entities_to_models(users: List[User]) -> List[UserModel]:
    models = [
        convert_entity_to_model(user)
        for user in users
    ]

    id2model = {model.id: model for model in models}

    for user in users:
        for ref in user.refs:
            model = id2model[user.pk]
            ref_model = id2model.get(ref.pk)

            if ref_model is not None:
                ref_model.parent = model

    return models


def convert_entity_to_model(entity: User) -> UserModel:
    return UserModel(
        id=entity.pk,
        ref_level=entity.ref_level.value,
        team_size=entity.team_size,
        balance=entity.balance,
    )


def convert_model_to_entity(model: UserModel) -> User:
    return User(
        pk=model.id,
        ref_level=RefLevel(model.ref_level),
        team_size=model.team_size,
        balance=model.balance,
        ref_pks=[ref.id for ref in model.refs.all()]
    )
