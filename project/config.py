from pathlib import Path
import os

BASE_DIR = Path(__file__).parent


class Config:
    DEBUG = bool(os.getenv("DEBUG", "0"))
    SECRET_KEY = str(os.getenv("SECRET_KEY"))
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = str(os.getenv("SQLALCHEMY_DATABASE_URI"))
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True