"""份额登记模型."""
from datetime import datetime

from models import db


class ShareRecord(db.Model):
    """投资者份额记录.

    存储投资者持有各基金产品的份额明细.
    """

    __tablename__ = "share_record"

    id = db.Column(db.Integer, primary_key=True)
    account_no = db.Column(
        db.String(32), nullable=False
    )
    fund_code = db.Column(
        db.String(16), nullable=False
    )
    total_shares = db.Column(
        db.Float, nullable=False, default=0.0
    )
    frozen_shares = db.Column(
        db.Float, nullable=False, default=0.0
    )
    available_shares = db.Column(
        db.Float, nullable=False, default=0.0
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "account_no", "fund_code",
            name="uq_account_fund",
        ),
    )

    def to_dict(self) -> dict:
        """转换为字典.

        Returns:
            dict: 包含份额信息的字典.
        """
        return {
            "account_no": self.account_no,
            "fund_code": self.fund_code,
            "total_shares": self.total_shares,
            "frozen_shares": self.frozen_shares,
            "available_shares": self.available_shares,
            "updated_at": (
                self.updated_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if self.updated_at
                else None
            ),
        }
