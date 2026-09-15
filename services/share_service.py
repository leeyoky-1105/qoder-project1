"""份额登记与查询服务."""
import logging
from datetime import datetime

from models import db
from models.share import ShareRecord

logger = logging.getLogger(__name__)


class ShareService:
    """份额管理服务.

    提供份额登记、增减、查询等功能.
    """

    @staticmethod
    def get_shares(account_no: str) -> dict:
        """查询投资者持有份额.

        Args:
            account_no: 交易账号.

        Returns:
            dict: 统一响应格式，包含份额列表.
        """
        records = ShareRecord.query.filter_by(
            account_no=account_no
        ).all()

        if not records:
            return {
                "code": 0,
                "message": "该账户暂无持有份额",
                "data": [],
            }

        return {
            "code": 0,
            "message": "success",
            "data": [r.to_dict() for r in records],
        }

    @staticmethod
    def add_shares(
        account_no: str,
        fund_code: str,
        shares: float,
    ) -> None:
        """增加投资者份额.

        Args:
            account_no: 交易账号.
            fund_code: 基金代码.
            shares: 增加的份额.
        """
        record = ShareRecord.query.filter_by(
            account_no=account_no,
            fund_code=fund_code,
        ).first()

        if record:
            record.total_shares += shares
            record.available_shares += shares
            record.updated_at = datetime.utcnow()
        else:
            record = ShareRecord(
                account_no=account_no,
                fund_code=fund_code,
                total_shares=shares,
                frozen_shares=0.0,
                available_shares=shares,
            )
            db.session.add(record)

        db.session.flush()
        logger.info(
            "份额增加: %s %s +%f",
            account_no, fund_code, shares,
        )

    @staticmethod
    def deduct_shares(
        account_no: str,
        fund_code: str,
        shares: float,
    ) -> str:
        """扣减投资者份额.

        Args:
            account_no: 交易账号.
            fund_code: 基金代码.
            shares: 扣减的份额.

        Returns:
            str: 错误信息，None 表示成功.
        """
        record = ShareRecord.query.filter_by(
            account_no=account_no,
            fund_code=fund_code,
        ).first()

        if not record:
            return "该账户无此基金持有份额"

        if record.available_shares < shares:
            return (
                f"可用份额不足，"
                f"当前可用 {record.available_shares:.2f}，"
                f"申请赎回 {shares:.2f}"
            )

        record.total_shares -= shares
        record.available_shares -= shares
        record.updated_at = datetime.utcnow()

        db.session.flush()
        logger.info(
            "份额扣减: %s %s -%f",
            account_no, fund_code, shares,
        )
        return None
