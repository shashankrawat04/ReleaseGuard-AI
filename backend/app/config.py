import os


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://releaseguard:local_dev_password@localhost:5432/releaseguard"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False