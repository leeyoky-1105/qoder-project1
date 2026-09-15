# 基金TA模拟登记系统

> qoder培训作业

模拟基金TA（注册登记）系统，支持投资者开户、基金申购/赎回、份额登记与对账等核心业务。

## 技术栈

- **后端**: Flask + SQLAlchemy
- **数据库**: SQLite
- **前端**: Jinja2 + Bootstrap 5
- **产品配置**: Excel 文件导入（openpyxl）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
python run.py
```

访问 http://localhost:5000 即可使用。

### 3. 导入基金产品

在首页点击"导入产品"按钮，从 Excel 文件导入基金产品信息，或调用 API：

```bash
curl -X POST http://localhost:5000/api/v1/funds/import
```

## 功能模块

| 模块 | 说明 | 入口 |
|------|------|------|
| 开户注册 | 四要素 + 手机号开户 | `/api/v1/accounts/register` |
| 基金列表 | 查看已导入的基金产品 | `/api/v1/funds/list` |
| 基金申购 | 选择基金，输入金额申购 | `/api/v1/trades/subscribe` |
| 基金赎回 | 选择基金，输入份额赎回 | `/api/v1/trades/redeem` |
| 份额查询 | 按账号查询持有份额 | `/api/v1/shares/query` |
| 对账报告 | 交易汇总与份额核对 | `/api/v1/reconciliation/report` |

## 基金产品

系统通过 `data/funds.xlsx` Excel 文件配置基金产品：

| 基金代码 | 基金名称 | 净值 | 净值日期 |
|----------|----------|------|----------|
| 000001 | 测试基金1 | 1.1012 | 20260915 |
| 000002 | 测试基金2 | 1.0032 | 20260916 |
| 000003 | 测试基金3 | 3.8923 | 20260917 |
| 000004 | 测试基金4 | 9.8971 | 20260918 |

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## 项目结构

```
fund-ta-system/
├── app.py              # 应用入口
├── config.py           # 配置
├── run.py              # 启动脚本
├── data/funds.xlsx     # 产品 Excel 配置
├── models/             # 数据模型
├── services/           # 业务服务
├── blueprints/         # API 路由
├── templates/          # 前端模板
└── tests/              # 单元测试
```
