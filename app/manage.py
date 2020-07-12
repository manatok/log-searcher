import os

from app import blueprint
from app.main import create_app

app = create_app(os.getenv('RUNNING_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()


def run():
    app.run(use_reloader=True, debug=False)


if __name__ == '__main__':
    run()
