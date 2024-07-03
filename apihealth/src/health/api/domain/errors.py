class ApplicationError(RuntimeError):
    message = "There was an unexpected error, if this error persist contact support."

    def __str__(self) -> str:
        return self.message


class EntityNotFound(ApplicationError):
    message = "We could not found the entity you are referencing"


class EntityAccessRestricted(ApplicationError):
    message = "You don't have access to the entity you are referencing."
