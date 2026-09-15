"""数据库查询脚本."""
import sqlite3

conn = sqlite3.connect("fund_ta.db")
cur = conn.cursor()

# 查看所有表
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("=== 数据库表 ===")
for r in cur.fetchall():
    print(f"  {r[0]}")
print()

# 查询各表数据
tables = {
    "investor_account": "投资者账户",
    "fund_product": "基金产品",
    "trade_order": "交易记录",
    "share_record": "份额登记",
}

for table, label in tables.items():
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    print(f"--- {label} ({table}): {count} 条记录 ---")
    if count > 0:
        cur.execute(f"SELECT * FROM {table}")
        cols = [d[0] for d in cur.description]
        print(f"  字段: {cols}")
        for row in cur.fetchall():
            print(f"  {row}")
    print()

conn.close()
