import psycopg2

from apihealth.src.health.api.services.helpers.project_util import \
    ProjectUtilHelper


class DatabaseConnection:
    def __init__(self):
        self._connection = None

    def __enter__(self):
        _project_util = ProjectUtilHelper()
        dbname = _project_util.get_runtime_env_variable("DB_NAME")
        user = _project_util.get_runtime_env_variable("DB_USER")
        password = _project_util.get_runtime_env_variable("DB_PASSWORD")
        host = _project_util.get_runtime_env_variable("DB_HOST")
        port = _project_util.get_runtime_env_variable("DB_PORT")

        self._connection = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        return self._connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self._connection:
            self._connection.close()
