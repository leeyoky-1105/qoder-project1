"""应用配置模块."""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基础配置."""

    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "fund-ta-dev-key-2026"
    )
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + os.path.join(BASE_DIR, "fund_ta.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FUNDS_CONFIG_PATH = os.path.join(
        BASE_DIR, "data", "funds.xlsx"
    )
