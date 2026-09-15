"""基金产品模型."""
from datetime import datetime

from models import db


class FundProduct(db.Model):
    """基金产品信息.

    存储基金产品核心要素，包括名称、代码、净值等.
    """

    __tablename__ = "fund_product"

    id = db.Column(db.Integer, primary_key=True)
    fund_code = db.Column(
        db.String(16), unique=True, nullable=False
    )
    fund_name = db.Column(
        db.String(64), nullable=False
    )
    nav = db.Column(db.Float, nullable=False)
    nav_date = db.Column(db.String(8), nullable=False)
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
            "nav": self.nav,
            "nav_date": self.nav_date,
            "status": self.status,
        }
