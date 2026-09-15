"""申购赎回交易服务."""
import logging
import random
import time
from datetime import datetime

from models import db
from models.account import InvestorAccount
from models.fund import FundProduct
from models.trade import TradeOrder
from services.share_service import ShareService

logger = logging.getLogger(__name__)

# 默认交易参数
DEFAULT_MIN_SUBSCRIBE = 1000.0
DEFAULT_MIN_REDEEM = 100.0
DEFAULT_SUBSCRIBE_FEE_RATE = 0.0
DEFAULT_REDEEM_FEE_RATE = 0.0


class TradeService:
    """交易管理服务.

    提供基金申购、赎回等交易功能.
    """

    @staticmethod
    def _generate_trade_no() -> str:
        """生成唯一交易流水号.

        Returns:
            str: 格式为 TRD + 时间戳 + 随机数.
        """
        ts = int(time.time() * 1000)
        rand = random.randint(1000, 9999)
        return f"TRD{ts}{rand}"

    @staticmethod
    def subscribe(
        account_no: str,
        fund_code: str,
        amount: float,
    ) -> dict:
        """基金申购.

        Args:
            account_no: 交易账号.
            fund_code: 基金代码.
            amount: 申购金额.

        Returns:
            dict: 统一响应格式，包含交易信息.
        """
        account = InvestorAccount.query.filter_by(
            account_no=account_no
        ).first()
        if not account:
            return {
                "code": 404,
                "message": "交易账户不存在",
                "data": None,
            }
        if account.status != "ACTIVE":
            return {
                "code": 400,
                "message": f"账户状态异常: {account.status}",
                "data": None,
            }

        fund = FundProduct.query.filter_by(
            fund_code=fund_code
        ).first()
        if not fund:
            return {
                "code": 404,
                "message": "基金产品不存在",
                "data": None,
            }
        if fund.status != "ACTIVE":
            return {
                "code": 400,
                "message": f"基金状态异常: {fund.status}",
                "data": None,
            }

        if amount < DEFAULT_MIN_SUBSCRIBE:
            return {
                "code": 400,
                "message": (
                    f"申购金额不得低于 "
                    f"{DEFAULT_MIN_SUBSCRIBE:.2f} 元"
                ),
                "data": None,
            }

        fee = round(
            amount * DEFAULT_SUBSCRIBE_FEE_RATE, 2
        )
        net_amount = amount - fee
        shares = round(net_amount / fund.nav, 2)

        trade = TradeOrder(
            trade_no=TradeService._generate_trade_no(),
            account_no=account_no,
            fund_code=fund_code,
            trade_type="SUBSCRIBE",
            amount=amount,
            nav=fund.nav,
            fee=fee,
            shares=shares,
            status="CONFIRMED",
            trade_time=datetime.utcnow(),
            confirm_time=datetime.utcnow(),
        )
        db.session.add(trade)

        ShareService.add_shares(
            account_no, fund_code, shares
        )

        db.session.commit()
        logger.info(
            "申购成功: %s %s 金额=%.2f 份额=%.2f",
            account_no, fund_code, amount, shares,
        )

        return {
            "code": 0,
            "message": "申购成功",
            "data": trade.to_dict(),
        }

    @staticmethod
    def redeem(
        account_no: str,
        fund_code: str,
        shares: float,
    ) -> dict:
        """基金赎回.

        Args:
            account_no: 交易账号.
            fund_code: 基金代码.
            shares: 赎回份额.

        Returns:
            dict: 统一响应格式，包含交易信息.
        """
        account = InvestorAccount.query.filter_by(
            account_no=account_no
        ).first()
        if not account:
            return {
                "code": 404,
                "message": "交易账户不存在",
                "data": None,
            }
        if account.status != "ACTIVE":
            return {
                "code": 400,
                "message": f"账户状态异常: {account.status}",
                "data": None,
            }

        fund = FundProduct.query.filter_by(
            fund_code=fund_code
        ).first()
        if not fund:
            return {
                "code": 404,
                "message": "基金产品不存在",
                "data": None,
            }
        if fund.status != "ACTIVE":
            return {
                "code": 400,
                "message": f"基金状态异常: {fund.status}",
                "data": None,
            }

        if shares < DEFAULT_MIN_REDEEM:
            return {
                "code": 400,
                "message": (
                    f"赎回份额不得低于 "
                    f"{DEFAULT_MIN_REDEEM:.2f} 份"
                ),
                "data": None,
            }

        err = ShareService.deduct_shares(
            account_no, fund_code, shares
        )
        if err:
            return {
                "code": 400,
                "message": err,
                "data": None,
            }

        amount = round(shares * fund.nav, 2)
        fee = round(
            amount * DEFAULT_REDEEM_FEE_RATE, 2
        )

        trade = TradeOrder(
            trade_no=TradeService._generate_trade_no(),
            account_no=account_no,
            fund_code=fund_code,
            trade_type="REDEEM",
            amount=amount,
            nav=fund.nav,
            fee=fee,
            shares=shares,
            status="CONFIRMED",
            trade_time=datetime.utcnow(),
            confirm_time=datetime.utcnow(),
        )
        db.session.add(trade)

        db.session.commit()
        logger.info(
            "赎回成功: %s %s 份额=%.2f 金额=%.2f",
            account_no, fund_code, shares, amount,
        )

        return {
            "code": 0,
            "message": "赎回成功",
            "data": trade.to_dict(),
        }

    @staticmethod
    def get_trade(trade_no: str) -> dict:
        """查询交易详情.

        Args:
            trade_no: 交易流水号.

        Returns:
            dict: 统一响应格式，包含交易信息.
        """
        trade = TradeOrder.query.filter_by(
            trade_no=trade_no
        ).first()

        if not trade:
            return {
                "code": 404,
                "message": "交易记录不存在",
                "data": None,
            }

        return {
            "code": 0,
            "message": "success",
            "data": trade.to_dict(),
        }

    @staticmethod
    def get_trades_by_account(
        account_no: str,
    ) -> list:
        """按账户查询交易记录.

        Args:
            account_no: 交易账号.

        Returns:
            list: 交易记录列表.
        """
        trades = TradeOrder.query.filter_by(
            account_no=account_no
        ).order_by(TradeOrder.trade_time.desc()).all()
        return [t.to_dict() for t in trades]
