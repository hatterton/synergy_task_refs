from refs.graph_loader import UserGraphLoader
from refs.entities import (
    User,
    RefLevel,
    UserGraph,
)
from refs.models import (
    UserModel,
)
from refs.mappers import (
    convert_from_entities_to_models,
    convert_from_models_to_entities,
    convert_model_to_entity,
)


class RefService:
    def __init__(self) -> None:
        self._graph_loader = UserGraphLoader()

    def get_user(self, pk: str) -> User:
        user_model = UserModel.objects.get(pk=pk)
        user = convert_model_to_entity(user_model)

        return user

    def load_and_save_user_graph(self, user_graph_data_path: str) -> UserGraph:
        user_graph = self._graph_loader.load(user_graph_data_path)

        users = list(user_graph.users)
        user_models = convert_from_entities_to_models(users)
        UserModel.objects.bulk_create(user_models)

        return user_graph

