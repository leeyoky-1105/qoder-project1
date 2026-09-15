"""账户服务单元测试."""
import sys
import os
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app import create_app
from models import db


class TestAccountService(unittest.TestCase):
    """账户服务测试."""

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

    def tearDown(self) -> None:
        """清理测试环境."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_success(self) -> None:
        """测试开户注册成功."""
        resp = self.client.post(
            "/api/v1/accounts/register",
            json={
                "name": "张三",
                "id_type": "身份证",
                "id_no": "110101199001011234",
                "bank_card_no": "6222021234567890123",
                "phone": "13800138000",
            },
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["code"], 0)
        self.assertEqual(data["message"], "开户成功")
        self.assertIn("account_no", data["data"])
        self.assertTrue(
            data["data"]["account_no"].startswith("ACC")
        )

    def test_register_duplicate_id(self) -> None:
        """测试同一证件号重复开户."""
        payload = {
            "name": "张三",
            "id_type": "身份证",
            "id_no": "110101199001011234",
            "bank_card_no": "6222021234567890123",
            "phone": "13800138000",
        }
        self.client.post(
            "/api/v1/accounts/register", json=payload
        )
        resp = self.client.post(
            "/api/v1/accounts/register", json=payload
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data["code"], 409)

    def test_register_invalid_phone(self) -> None:
        """测试无效手机号."""
        resp = self.client.post(
            "/api/v1/accounts/register",
            json={
                "name": "张三",
                "id_type": "身份证",
                "id_no": "110101199001011234",
                "bank_card_no": "6222021234567890123",
                "phone": "12345",
            },
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data["code"], 400)

    def test_register_missing_fields(self) -> None:
        """测试缺失必填字段."""
        resp = self.client.post(
            "/api/v1/accounts/register",
            json={"name": "张三"},
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data["code"], 400)

    def test_get_account(self) -> None:
        """测试查询账户信息."""
        reg_resp = self.client.post(
            "/api/v1/accounts/register",
            json={
                "name": "李四",
                "id_type": "护照",
                "id_no": "E12345678",
                "bank_card_no": "6222021234567890456",
                "phone": "13900139000",
            },
        )
        account_no = reg_resp.get_json()["data"]["account_no"]

        resp = self.client.get(
            f"/api/v1/accounts/{account_no}"
        )
        data = resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["data"]["name"], "李四")

    def test_get_account_not_found(self) -> None:
        """测试查询不存在的账户."""
        resp = self.client.get("/api/v1/accounts/ACC000")
        data = resp.get_json()
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
