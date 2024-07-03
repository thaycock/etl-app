import inspect
import logging
import os
import subprocess
import uuid
from uuid import UUID


class ContextManager:
    """
         the constructor is called with successfull instantiation of the object
        and defines what files context manager class can be used by which is only
        the util class to avoid littering the code base with direct calls to OS
        module or other modules that are commonly used during runtime.
        This mitigates the risk of this and employs a style to obtain this type
        of information.

    Raises:
        RuntimeError: if the enviornment is unables to be configured properly or
        illegal env state
        OSError: raised if unregisterd called tries to call the method or any
        class that is not util
        OSError: raised if the system in not able to run a requested os command
        OSError: raised if an environment variable is not present or un-obtainable
        RuntimeError: [description]

    Returns:
        [type]: [description]
    """

    ALLOWED_STATES: list = ["UNITTEST", "DEV", "PROD"]

    def __init__(self) -> None:
        """
        second string in the arrays are for the tests because the caller id is of a different origin
        but ultimatley calling the same file
        """
        self._permissions = {
            "register": [
                "apihealth.src.health.api.app",
                "apihealth.src.health.api.services.helpers.project_util",
            ],
            "system": {
                subprocess: [
                    "apihealth.src.health.api.app",
                    "apihealth.src.health.api.services.helpers.project_util",
                ]
            },
            "environ": {
                os.getenv: [
                    "apihealth.src.health.api.app",
                    "apihealth.src.health.api.services.helpers.project_util",
                ]
            },
        }
        self.caller_id = inspect.getmodule(inspect.stack()[1][0]).__name__
        logging.info("Context manager entered from %s", self.caller_id)

    def _configure_env(self) -> None:
        """
        performs verification of a legal environment runtime state of the application

        Raises:
        RuntimeError: raises illegal runtime error
        """
        runtime_env = os.getenv("RUNTIME_ENVIRONMENT")
        if runtime_env not in self.ALLOWED_STATES:
            logging.critical("Unexpected data runtime state. Exiting..")
            # raise RuntimeError("Unknown or illegal runtime env! {}".format(runtime_env))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def register(self) -> None:
        """
        Registers the os environment variables by generating a hash of the
        environment variables, and pushing it to the environment variables.
        This registration should only be called at the
        top level system __init__. This is a one time function call for a
        system runtime instance.
        """
        # verify caller id is registered to perform env registration
        if self.caller_id not in self._permissions["register"]:
            logging.warning(
                "Revoked unregistered caller %s permissions to register environment",
                self.caller_id,
            )

            logging.error(
                "Unregistered caller {} list of authorized callers:{}".format(
                    self.caller_id, self._permissions
                )
            )
            raise OSError
        self._configure_env()
        os.environ["ENV_HASH"] = self.__get_env_hash()
        logging.info(
            "Created first-time environment registration hash from %s", self.caller_id
        )
        logging.info("Environment hash: %s", os.environ.get("ENV_HASH"))

    def run_os_command(self, cmd: tuple) -> list:
        """
        runs the os command as long as the module or file is registered in the context manager
        called like this  i.e context.run_os_command('system')('echo hello world')
        """
        cmd_name: str = cmd[0]
        cmd_arg: str = cmd[1]
        legal_accessors: list = list(self._permissions[cmd_name].values())[0]
        if self.caller_id not in legal_accessors:
            logging.warning(
                "Revoked unregistered caller {} permissions to execute os methods".format(
                    self.caller_id
                )
            )
            raise OSError
        try:
            self._permissions[cmd_name]
            return subprocess.run([cmd_arg])
        except KeyError as err:
            logging.exception("Unregistered command: {}".format(err))
        except NameError as err:
            logging.exception("Unable to access environment variable: {}".format(err))

    def fetch_environment_variable(self, env_var: tuple) -> str:
        """
        fetches the requested environment variable after the appropriate logical verification
        process of resource management access.
        Args:
            env_var (str): requested env varibale
        Raises:
            RuntimeError: if critical env variable cannot be found
        Returns:
            str: env varibales value
        """
        env_name: str = env_var[0]
        env_value: str = env_var[1]
        legal_accessors: list = list(self._permissions[env_name].values())[0]
        if self.caller_id not in legal_accessors:
            logging.warning(
                "Revoked unregistered caller {} permissions to execute os methods".format(
                    self.caller_id
                )
            )
            raise OSError
        try:
            self._permissions[env_name]
            if env_value in os.environ:
                return os.getenv(env_value)
            else:
                raise RuntimeError(
                    "Unable to get requested environment variable! {}".format(env_value)
                )
        except (KeyError,) as err:
            logging.exception("Unregistered command: {}".format(err))
        except NameError as err:
            logging.exception("Unable to access environment variable: {}".format(err))

    def __get_env_hash(self) -> str:
        # Generate a UUID version 4
        return str(uuid.uuid4())
