class BaseConfig(object):
    """Base configuration."""
    WTF_CSRF_ENABLED = True
    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]
    # Exchanges
    # BINANCE_KEY = os_get("BINANCE_KEY")
    # BINANCE_SECRET = os_get("BINANCE_SECRET")
    # BITMEX_KEY = os_get("BITMEX_KEY")
    # BITMEX_SECRET = os_get("BITMEX_SECRET")
    # Database
    # SQLALCHEMY_DATABASE_URI = os_get("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_ECHO = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    WTF_CSRF_ENABLED = False


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
