from dependency_injector import containers, providers

from app.database import get_db


class DependencyContainer(containers.DeclarativeContainer):
    session = providers.Factory(get_db)


container = DependencyContainer()
