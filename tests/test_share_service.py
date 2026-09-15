"""份额服务单元测试."""
import sys
import os
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app import create_app
from models import db
from services.fund_loader import FundLoaderService


class TestShareService(unittest.TestCase):
    """份额服务测试."""

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
                "name": "赵六",
                "id_type": "身份证",
                "id_no": "440101199203031234",
                "bank_card_no": "622202555566667777",
                "phone": "13600136000",
            },
        )
        self.account_no = resp.get_json()["data"]["account_no"]

    def tearDown(self) -> None:
        """清理测试环境."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_query_shares_empty(self) -> None:
        """测试查询空份额."""
        resp = self.client.get(
            f"/api/v1/shares/{self.account_no}"
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["data"], [])

    def test_shares_after_subscribe(self) -> None:
        """测试申购后份额增加."""
        self.client.post(
            "/api/v1/trades/subscribe",
            json={
                "account_no": self.account_no,
                "fund_code": "000001",
                "amount": 10000,
            },
        )

        resp = self.client.get(
            f"/api/v1/shares/{self.account_no}"
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["fund_code"], "000001")
        self.assertGreater(data["data"][0]["total_shares"], 0)

    def test_shares_after_redeem(self) -> None:
        """测试赎回后份额减少."""
        self.client.post(
            "/api/v1/trades/subscribe",
            json={
                "account_no": self.account_no,
                "fund_code": "000001",
                "amount": 50000,
            },
        )

        subscribe_resp = self.client.get(
            f"/api/v1/shares/{self.account_no}"
        )
        shares_before = subscribe_resp.get_json()["data"][0]["total_shares"]

        self.client.post(
            "/api/v1/trades/redeem",
            json={
                "account_no": self.account_no,
                "fund_code": "000001",
                "shares": 1000,
            },
        )

        resp = self.client.get(
            f"/api/v1/shares/{self.account_no}"
        )
        shares_after = resp.get_json()["data"][0]["total_shares"]
        self.assertAlmostEqual(
            shares_before - shares_after, 1000.0, places=1
        )

    def test_reconciliation_report(self) -> None:
        """测试对账报告."""
        self.client.post(
            "/api/v1/trades/subscribe",
            json={
                "account_no": self.account_no,
                "fund_code": "000001",
                "amount": 20000,
            },
        )

        resp = self.client.get(
            "/api/v1/reconciliation/report/json"
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data["data"]["all_match"])


if __name__ == "__main__":
    unittest.main()
