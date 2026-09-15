"""启动脚本 - 初始化数据库并启动应用."""
from app import create_app
from models import db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    db.create_all()
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Database tables: {tables}")

app.run(debug=True, port=5000, use_reloader=False)
