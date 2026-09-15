"""投资者账户服务."""
import logging
import random
import time

from models import db
from models.account import InvestorAccount

logger = logging.getLogger(__name__)

ID_TYPE_OPTIONS = ["身份证", "护照", "军官证"]


class AccountService:
    """投资者账户管理服务.

    提供开户注册、账户查询等功能.
    """

    @staticmethod
    def _generate_account_no() -> str:
        """生成唯一交易账号.

        Returns:
            str: 格式为 ACC + 时间戳 + 随机数.
        """
        ts = int(time.time() * 1000)
        rand = random.randint(1000, 9999)
        return f"ACC{ts}{rand}"

    @staticmethod
    def register(
        name: str,
        id_type: str,
        id_no: str,
        bank_card_no: str,
        phone: str,
    ) -> dict:
        """投资者开户注册.

        Args:
            name: 投资者姓名.
            id_type: 证件类型.
            id_no: 证件号码.
            bank_card_no: 银行卡号.
            phone: 手机号.

        Returns:
            dict: 统一响应格式，包含账号信息.
        """
        if not all([name, id_type, id_no, bank_card_no, phone]):
            return {
                "code": 400,
                "message": "所有字段均为必填项",
                "data": None,
            }

        if id_type not in ID_TYPE_OPTIONS:
            return {
                "code": 400,
                "message": f"证件类型无效，可选: {ID_TYPE_OPTIONS}",
                "data": None,
            }

        if not phone.isdigit() or len(phone) != 11:
            return {
                "code": 400,
                "message": "手机号格式无效，需11位数字",
                "data": None,
            }

        existing = InvestorAccount.query.filter_by(
            id_no=id_no
        ).first()
        if existing:
            return {
                "code": 409,
                "message": "该证件号码已开户，不可重复开户",
                "data": None,
            }

        account = InvestorAccount(
            account_no=AccountService._generate_account_no(),
            name=name,
            id_type=id_type,
            id_no=id_no,
            bank_card_no=bank_card_no,
            phone=phone,
            status="ACTIVE",
        )
        db.session.add(account)
        db.session.commit()

        logger.info("开户成功: %s", account.account_no)
        return {
            "code": 0,
            "message": "开户成功",
            "data": account.to_dict(),
        }

    @staticmethod
    def get_account(account_no: str) -> dict:
        """查询账户信息.

        Args:
            account_no: 交易账号.

        Returns:
            dict: 统一响应格式，包含账户信息.
        """
        account = InvestorAccount.query.filter_by(
            account_no=account_no
        ).first()

        if not account:
            return {
                "code": 404,
                "message": "账户不存在",
                "data": None,
            }

        return {
            "code": 0,
            "message": "success",
            "data": account.to_dict(),
        }

    @staticmethod
    def get_all_accounts() -> list:
        """获取所有账户列表.

        Returns:
            list: 账户列表.
        """
        accounts = InvestorAccount.query.all()
        return [acc.to_dict() for acc in accounts]
