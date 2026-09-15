"""数据模型包."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.account import InvestorAccount  # noqa: E402, F401
from models.fund import FundProduct  # noqa: E402, F401
from models.trade import TradeOrder  # noqa: E402, F401
from models.share import ShareRecord  # noqa: E402, F401
