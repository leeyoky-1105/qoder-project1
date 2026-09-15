"""基金TA注册系统 - Flask 应用入口."""
from flask import Flask, jsonify, render_template

from config import Config
from models import db
from models.fund import FundProduct
from services.fund_loader import FundLoaderService


def create_app() -> Flask:
    """创建并配置 Flask 应用.

    Returns:
        Flask: 配置完成的 Flask 应用实例.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from blueprints.account import account_bp
    from blueprints.trade import trade_bp
    from blueprints.share import share_bp
    from blueprints.reconciliation import recon_bp

    app.register_blueprint(account_bp)
    app.register_blueprint(trade_bp)
    app.register_blueprint(share_bp)
    app.register_blueprint(recon_bp)

    @app.route("/")
    def index():
        """首页导航."""
        return render_template("index.html")

    @app.route("/api/v1/funds", methods=["GET"])
    def list_funds():
        """查询基金产品列表."""
        funds = FundProduct.query.all()
        return jsonify({
            "code": 0,
            "message": "success",
            "data": [f.to_dict() for f in funds],
        })

    @app.route("/api/v1/funds/list", methods=["GET"])
    def list_funds_page():
        """基金产品列表页面."""
        funds = FundProduct.query.all()
        return render_template(
            "fund/list.html",
            funds=[f.to_dict() for f in funds],
        )

    @app.route("/api/v1/funds/import", methods=["POST"])
    def import_funds():
        """导入基金产品配置."""
        config_path = app.config["FUNDS_CONFIG_PATH"]
        result = FundLoaderService.import_funds(config_path)
        return jsonify(result), (
            200 if result["code"] == 0 else 400
        )

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
