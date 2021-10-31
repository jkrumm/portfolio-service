import logging
import os

import sentry_sdk
from flask import Flask
from flask_bootstrap import Bootstrap
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.rq import RqIntegration

bootstrap = Bootstrap()


def create_app(script_info=None):
    # All of this is already happening by default!
    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY'),
        integrations=[FlaskIntegration(), RqIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

    # instantiate the app
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # db.init_app(app)

    # PrometheusMetrics(app)

    # set up extensions
    bootstrap.init_app(app)

    # register blueprints
    from project.server.main.views import main_blueprint

    app.register_blueprint(main_blueprint)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app
