from apihealth.src.health.api.services.helpers.project_util import \
    ProjectUtilHelper
from apihealth.src.health.api.services.loaders.etl_loader import ETLLoader
from apihealth.src.health.api.services.query_services.data_loader_queries import \
    DataLoaderQueries


class ETLMigrationHandler(ProjectUtilHelper):
    def __init__(self) -> None:
        self._data_loader = DataLoaderQueries()
        source_url = self.get_runtime_env_variable("DATA_SOURCE")
        self._etl_loader = ETLLoader(source_url)

    def start_data_migration_service(self) -> None:
        """
        Entry method to load data
        """
        event_data = self._etl_loader.load_data_from_endpoint()
        self._data_loader.load_data_to_table(event_data)

    def get_latest_event_data(self):
        """
        fetches the latest us event data from the database

        Returns:
            list: collection of rows
        """
        return self._data_loader.fetch_latest_event_data()
