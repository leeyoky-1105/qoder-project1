"""份额查询路由."""
from flask import Blueprint, jsonify, render_template, request

from services.share_service import ShareService
from services.trade_service import TradeService

share_bp = Blueprint(
    "share", __name__,
    url_prefix="/api/v1/shares",
)


@share_bp.route("/query", methods=["GET"])
def query_page():
    """份额查询页面."""
    account_no = request.args.get("account_no", "")
    shares_data = None
    trades = None

    if account_no:
        result = ShareService.get_shares(account_no)
        shares_data = result.get("data", [])
        trades = TradeService.get_trades_by_account(
            account_no
        )

    return render_template(
        "share/query.html",
        shares=shares_data,
        trades=trades,
        account_no=account_no,
    )


@share_bp.route("/<account_no>", methods=["GET"])
def get_shares(account_no: str):
    """查询持有份额."""
    result = ShareService.get_shares(account_no)
    return jsonify(result)
