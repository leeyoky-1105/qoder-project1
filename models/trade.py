"""交易记录模型."""
from datetime import datetime

from models import db


class TradeOrder(db.Model):
    """交易订单记录.

    存储申购、赎回等交易流水信息.
    """

    __tablename__ = "trade_order"

    id = db.Column(db.Integer, primary_key=True)
    trade_no = db.Column(
        db.String(32), unique=True, nullable=False
    )
    account_no = db.Column(
        db.String(32), nullable=False
    )
    fund_code = db.Column(
        db.String(16), nullable=False
    )
    trade_type = db.Column(
        db.String(16), nullable=False
    )
    amount = db.Column(db.Float, nullable=False)
    nav = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    shares = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.String(16), nullable=False,
        default="PENDING",
    )
    trade_time = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    confirm_time = db.Column(db.DateTime, nullable=True)

    def to_dict(self) -> dict:
        """转换为字典.

        Returns:
            dict: 包含交易信息的字典.
        """
        return {
            "trade_no": self.trade_no,
            "account_no": self.account_no,
            "fund_code": self.fund_code,
            "trade_type": self.trade_type,
            "amount": self.amount,
            "nav": self.nav,
            "fee": self.fee,
            "shares": self.shares,
            "status": self.status,
            "trade_time": (
                self.trade_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if self.trade_time
                else None
            ),
            "confirm_time": (
                self.confirm_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if self.confirm_time
                else None
            ),
        }
