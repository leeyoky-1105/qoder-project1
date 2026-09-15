"""投资者账户模型."""
from datetime import datetime

from models import db


class InvestorAccount(db.Model):
    """投资者账户信息.

    存储投资者开户时提交的四要素及手机号等核心信息.
    """

    __tablename__ = "investor_account"

    id = db.Column(db.Integer, primary_key=True)
    account_no = db.Column(
        db.String(32), unique=True, nullable=False
    )
    name = db.Column(
        db.String(64), nullable=False
    )
    id_type = db.Column(
        db.String(16), nullable=False
    )
    id_no = db.Column(
        db.String(32), nullable=False
    )
    bank_card_no = db.Column(
        db.String(32), nullable=False
    )
    phone = db.Column(
        db.String(16), nullable=False
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
            dict: 包含账户信息的字典.
        """
        return {
            "account_no": self.account_no,
            "name": self.name,
            "id_type": self.id_type,
            "id_no": self.id_no,
            "bank_card_no": self.bank_card_no,
            "phone": self.phone,
            "status": self.status,
            "created_at": (
                self.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if self.created_at
                else None
            ),
        }
