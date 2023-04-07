from refs.urls import RefServiceConfig
from refs.service import RefService


def load_user_graph_data() -> None:
    config = RefServiceConfig()
    service = RefService()

    service.load_and_save_user_graph(config.user_graph_data_path)
