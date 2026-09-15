"""交易相关路由."""
from flask import Blueprint, jsonify, render_template, request

from models.fund import FundProduct
from services.account_service import AccountService
from services.trade_service import TradeService

trade_bp = Blueprint(
    "trade", __name__,
    url_prefix="/api/v1/trades",
)


@trade_bp.route("/subscribe", methods=["GET"])
def subscribe_page():
    """申购下单页面."""
    funds = FundProduct.query.all()
    accounts = AccountService.get_all_accounts()
    return render_template(
        "trade/subscribe.html",
        funds=[f.to_dict() for f in funds],
        accounts=accounts,
    )


@trade_bp.route("/subscribe", methods=["POST"])
def subscribe():
    """申购下单接口."""
    data = request.get_json() or request.form.to_dict()

    result = TradeService.subscribe(
        account_no=data.get("account_no", ""),
        fund_code=data.get("fund_code", ""),
        amount=float(data.get("amount", 0)),
    )

    if request.is_json:
        return jsonify(result), (
            200 if result["code"] == 0 else 400
        )

    if result["code"] == 0:
        return render_template(
            "trade/detail.html",
            success=True,
            trade=result["data"],
            trade_type="申购",
        )

    funds = FundProduct.query.all()
    accounts = AccountService.get_all_accounts()
    return render_template(
        "trade/subscribe.html",
        funds=[f.to_dict() for f in funds],
        accounts=accounts,
        error=result["message"],
    )


@trade_bp.route("/redeem", methods=["GET"])
def redeem_page():
    """赎回下单页面."""
    funds = FundProduct.query.all()
    accounts = AccountService.get_all_accounts()
    return render_template(
        "trade/redeem.html",
        funds=[f.to_dict() for f in funds],
        accounts=accounts,
    )


@trade_bp.route("/redeem", methods=["POST"])
def redeem():
    """赎回下单接口."""
    data = request.get_json() or request.form.to_dict()

    result = TradeService.redeem(
        account_no=data.get("account_no", ""),
        fund_code=data.get("fund_code", ""),
        shares=float(data.get("shares", 0)),
    )

    if request.is_json:
        return jsonify(result), (
            200 if result["code"] == 0 else 400
        )

    if result["code"] == 0:
        return render_template(
            "trade/detail.html",
            success=True,
            trade=result["data"],
            trade_type="赎回",
        )

    funds = FundProduct.query.all()
    accounts = AccountService.get_all_accounts()
    return render_template(
        "trade/redeem.html",
        funds=[f.to_dict() for f in funds],
        accounts=accounts,
        error=result["message"],
    )


@trade_bp.route("/<trade_no>", methods=["GET"])
def get_trade(trade_no: str):
    """查询交易详情."""
    result = TradeService.get_trade(trade_no)
    return jsonify(result), (
        200 if result["code"] == 0 else 404
    )


@trade_bp.route("/account/<account_no>", methods=["GET"])
def get_trades_by_account(account_no: str):
    """按账户查询交易记录."""
    trades = TradeService.get_trades_by_account(account_no)
    return jsonify({
        "code": 0,
        "message": "success",
        "data": trades,
    })
