"""创建基金信息 Excel 模板文件."""
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Sheet1"

# 表头
headers = ["基金名称", "基金代码", "基金净值", "净值日期"]
ws.append(headers)

# 数据
data = [
    ["测试基金1", "000001", 1.1012, "20260915"],
    ["测试基金2", "000002", 1.0032, "20260916"],
    ["测试基金3", "000003", 3.8923, "20260917"],
    ["测试基金4", "000004", 9.8971, "20260918"],
]
for row in data:
    ws.append(row)

wb.save("data/funds.xlsx")
print("Excel 模板文件已创建: data/funds.xlsx")
