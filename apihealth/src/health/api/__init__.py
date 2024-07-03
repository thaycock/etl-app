from .app import create_app

app = create_app(
    __name__,
    autoload_blueprints=True,
    blueprints_module="blueprints",
    host="0.0.0.0",
)
