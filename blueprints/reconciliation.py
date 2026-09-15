"""对账路由."""
from flask import Blueprint, jsonify, render_template

from services.reconciliation_service import ReconciliationService

recon_bp = Blueprint(
    "reconciliation", __name__,
    url_prefix="/api/v1/reconciliation",
)


@recon_bp.route("/report", methods=["GET"])
def report_page():
    """对账报告页面."""
    result = ReconciliationService.generate_report()
    return render_template(
        "reconciliation/report.html",
        report=result["data"],
    )


@recon_bp.route("/report/json", methods=["GET"])
def report_json():
    """对账报告 JSON 接口."""
    result = ReconciliationService.generate_report()
    return jsonify(result)
