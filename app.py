"""基金TA注册系统 - Flask 应用入口."""
from flask import Flask, render_template

from config import Config
from models import db


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

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
