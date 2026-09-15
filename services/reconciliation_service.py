"""对账服务."""
import logging

from models.fund import FundProduct
from models.share import ShareRecord
from models.trade import TradeOrder

logger = logging.getLogger(__name__)


class ReconciliationService:
    """对账管理服务.

    提供交易对账、份额核对等功能.
    """

    @staticmethod
    def generate_report() -> dict:
        """生成对账报告.

        Returns:
            dict: 统一响应格式，包含对账报告数据.
        """
        funds = FundProduct.query.all()
        report_items = []

        for fund in funds:
            trades = TradeOrder.query.filter_by(
                fund_code=fund.fund_code
            ).all()

            subscribe_trades = [
                t for t in trades
                if t.trade_type == "SUBSCRIBE"
                and t.status == "CONFIRMED"
            ]
            redeem_trades = [
                t for t in trades
                if t.trade_type == "REDEEM"
                and t.status == "CONFIRMED"
            ]

            total_subscribe_amount = sum(
                t.amount for t in subscribe_trades
            )
            total_redeem_amount = sum(
                t.amount for t in redeem_trades
            )
            total_subscribe_shares = sum(
                t.shares for t in subscribe_trades
            )
            total_redeem_shares = sum(
                t.shares for t in redeem_trades
            )
            total_fee = sum(t.fee for t in trades)

            share_records = ShareRecord.query.filter_by(
                fund_code=fund.fund_code
            ).all()
            total_held_shares = sum(
                r.total_shares for r in share_records
            )

            expected_shares = (
                total_subscribe_shares
                - total_redeem_shares
            )
            shares_match = abs(
                total_held_shares - expected_shares
            ) < 0.01

            report_items.append({
                "fund_code": fund.fund_code,
                "fund_name": fund.fund_name,
                "fund_type": fund.fund_type,
                "nav": fund.nav,
                "subscribe_count": len(subscribe_trades),
                "subscribe_amount": round(
                    total_subscribe_amount, 2
                ),
                "subscribe_shares": round(
                    total_subscribe_shares, 2
                ),
                "redeem_count": len(redeem_trades),
                "redeem_amount": round(
                    total_redeem_amount, 2
                ),
                "redeem_shares": round(
                    total_redeem_shares, 2
                ),
                "total_fee": round(total_fee, 2),
                "total_held_shares": round(
                    total_held_shares, 2
                ),
                "expected_shares": round(
                    expected_shares, 2
                ),
                "shares_match": shares_match,
                "investor_count": len(share_records),
            })

        all_match = all(
            item["shares_match"]
            for item in report_items
        )

        return {
            "code": 0,
            "message": "success",
            "data": {
                "items": report_items,
                "all_match": all_match,
                "total_funds": len(report_items),
            },
        }
