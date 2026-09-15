"""基金产品模型."""
from datetime import datetime

from models import db


class FundProduct(db.Model):
    """基金产品信息.

    存储基金产品核心要素，包括净值、费率等.
    """

    __tablename__ = "fund_product"

    id = db.Column(db.Integer, primary_key=True)
    fund_code = db.Column(
        db.String(16), unique=True, nullable=False
    )
    fund_name = db.Column(
        db.String(64), nullable=False
    )
    fund_type = db.Column(
        db.String(16), nullable=False
    )
    nav = db.Column(db.Float, nullable=False)
    nav_date = db.Column(db.Date, nullable=False)
    min_subscribe = db.Column(
        db.Float, nullable=False, default=1000.0
    )
    min_redeem = db.Column(
        db.Float, nullable=False, default=100.0
    )
    subscribe_fee_rate = db.Column(
        db.Float, nullable=False, default=0.0
    )
    redeem_fee_rate = db.Column(
        db.Float, nullable=False, default=0.0
    )
    status = db.Column(
        db.String(8), nullable=False, default="ACTIVE"
    )
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )

    def to_dict(self) -> dict:
        """转换为字典.

        Returns:
            dict: 包含产品信息的字典.
        """
        return {
            "fund_code": self.fund_code,
            "fund_name": self.fund_name,
            "fund_type": self.fund_type,
            "nav": self.nav,
            "nav_date": (
                self.nav_date.strftime("%Y-%m-%d")
                if self.nav_date
                else None
            ),
            "min_subscribe": self.min_subscribe,
            "min_redeem": self.min_redeem,
            "subscribe_fee_rate": self.subscribe_fee_rate,
            "redeem_fee_rate": self.redeem_fee_rate,
            "status": self.status,
        }
