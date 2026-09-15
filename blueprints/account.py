"""账户相关路由."""
from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
)

from models.fund import FundProduct
from services.account_service import AccountService
from services.fund_loader import FundLoaderService

account_bp = Blueprint(
    "account", __name__,
    url_prefix="/api/v1/accounts",
)


@account_bp.route("/register", methods=["GET"])
def register_page():
    """开户注册页面."""
    return render_template("account/register.html")


@account_bp.route("/register", methods=["POST"])
def register():
    """开户注册接口."""
    data = request.get_json() or request.form.to_dict()

    result = AccountService.register(
        name=data.get("name", ""),
        id_type=data.get("id_type", ""),
        id_no=data.get("id_no", ""),
        bank_card_no=data.get("bank_card_no", ""),
        phone=data.get("phone", ""),
    )

    if request.is_json:
        return jsonify(result), (
            200 if result["code"] == 0 else 400
        )

    if result["code"] == 0:
        return render_template(
            "account/register.html",
            success=True,
            account=result["data"],
        )
    return render_template(
        "account/register.html",
        success=False,
        error=result["message"],
    )


@account_bp.route("/<account_no>", methods=["GET"])
def get_account(account_no: str):
    """查询账户信息."""
    result = AccountService.get_account(account_no)
    return jsonify(result), (
        200 if result["code"] == 0 else 404
    )


@account_bp.route("/import-funds", methods=["POST"])
def import_funds():
    """导入基金产品配置."""
    config_path = current_app.config["FUNDS_CONFIG_PATH"]
    result = FundLoaderService.import_funds(config_path)
    return jsonify(result), (
        200 if result["code"] == 0 else 400
    )


@account_bp.route("/funds", methods=["GET"])
def list_funds():
    """查询基金产品列表."""
    funds = FundProduct.query.all()
    return jsonify({
        "code": 0,
        "message": "success",
        "data": [f.to_dict() for f in funds],
    })


@account_bp.route("/list", methods=["GET"])
def list_accounts():
    """查询所有账户."""
    accounts = AccountService.get_all_accounts()
    return jsonify({
        "code": 0,
        "message": "success",
        "data": accounts,
    })
