"""交易服务单元测试."""
import sys
import os
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app import create_app
from models import db
from services.fund_loader import FundLoaderService


class TestTradeService(unittest.TestCase):
    """交易服务测试."""

    def setUp(self) -> None:
        """初始化测试环境."""
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///:memory:"
        )
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            FundLoaderService.import_funds(
                self.app.config["FUNDS_CONFIG_PATH"]
            )

        resp = self.client.post(
            "/api/v1/accounts/register",
            json={
                "name": "王五",
                "id_type": "身份证",
                "id_no": "310101199505051234",
                "bank_card_no": "622202333344445555",
                "phone": "13700137000",
            },
        )
        self.account_no = resp.get_json()["data"]["account_no"]

    def tearDown(self) -> None:
        """清理测试环境."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_subscribe_success(self) -> None:
        """测试申购成功."""
        resp = self.client.post(
            "/api/v1/trades/subscribe",
            json={
                "account_no": self.account_no,
                "fund_code": "000001",
                "amount": 10000,
            },
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["code"], 0)
        self.assertEqual(data["data"]["trade_type"], "SUBSCRIBE")
        self.assertGreater(data["data"]["shares"], 0)

    def test_subscribe_below_minimum(self) -> None:
        """测试申购金额低于最低限额."""
        resp = self.client.post(
            "/api/v1/trades/subscribe",
            json={
                "account_no": self.account_no,
                "fund_code": "000001",
                "amount": 100,
            },
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data["code"], 400)

    def test_redeem_success(self) -> None:
        """测试赎回成功."""
        self.client.post(
            "/api/v1/trades/subscribe",
            json={
                "account_no": self.account_no,
                "fund_code": "000002",
                "amount": 50000,
            },
        )

        resp = self.client.post(
            "/api/v1/trades/redeem",
            json={
                "account_no": self.account_no,
                "fund_code": "000002",
                "shares": 1000,
            },
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["code"], 0)
        self.assertEqual(data["data"]["trade_type"], "REDEEM")

    def test_redeem_insufficient_shares(self) -> None:
        """测试赎回份额不足."""
        resp = self.client.post(
            "/api/v1/trades/redeem",
            json={
                "account_no": self.account_no,
                "fund_code": "000001",
                "shares": 1000,
            },
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 400)

    def test_subscribe_invalid_account(self) -> None:
        """测试无效账户申购."""
        resp = self.client.post(
            "/api/v1/trades/subscribe",
            json={
                "account_no": "ACC_INVALID",
                "fund_code": "000001",
                "amount": 10000,
            },
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data["code"], 404)


if __name__ == "__main__":
    unittest.main()
