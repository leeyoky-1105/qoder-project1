# 模拟基金TA注册系统实施计划（已更新）

## 项目概述

构建一个模拟基金TA（注册登记）系统，支持投资者开户、基金申购/赎回交易、份额登记与对账、交易及份额查询。采用 Flask + SQLite + Bootstrap 技术栈，产品数据通过 Excel 文件配置导入。

## 技术架构

| 层级 | 技术选型 |
|------|---------|
| 后端框架 | Flask + Blueprint |
| 数据库 | SQLite + SQLAlchemy |
| 前端 | Jinja2 模板 + Bootstrap 5 + 原生 JS |
| 产品配置 | Excel 文件导入（openpyxl） |
| 代码管理 | Git + GitHub |

## 目录结构

```
fund-ta-system/
├── app.py                      # Flask 应用入口
├── config.py                   # 应用配置
├── requirements.txt            # Python 依赖
├── .gitignore
├── README.md
├── data/
│   └── funds.xlsx              # 基金产品 Excel 配置文件
├── models/
│   ├── __init__.py
│   ├── account.py              # 账户模型（投资者信息）
│   ├── fund.py                 # 基金产品模型
│   ├── trade.py                # 交易记录模型
│   └── share.py                # 份额登记模型
├── services/
│   ├── __init__.py
│   ├── account_service.py      # 开户/账户查询服务
│   ├── trade_service.py        # 申购/赎回交易服务
│   ├── share_service.py        # 份额登记/查询服务
│   ├── reconciliation_service.py  # 对账服务
│   └── fund_loader.py          # 产品文件导入服务（Excel）
├── blueprints/
│   ├── __init__.py
│   ├── account.py              # 账户相关路由
│   ├── trade.py                # 交易相关路由
│   ├── share.py                # 份额查询路由
│   └── reconciliation.py       # 对账路由
├── templates/
│   ├── base.html               # 基础布局
│   ├── index.html              # 首页/导航
│   ├── account/
│   │   └── register.html       # 开户注册页面
│   ├── fund/
│   │   └── list.html           # 基金产品列表页面
│   ├── trade/
│   │   ├── subscribe.html      # 申购下单页面
│   │   ├── redeem.html         # 赎回下单页面
│   │   └── detail.html         # 交易详情/结果页
│   ├── share/
│   │   └── query.html          # 份额查询页面
│   └── reconciliation/
│       └── report.html         # 对账报告页面
└── tests/
    ├── __init__.py
    ├── test_account_service.py
    ├── test_trade_service.py
    └── test_share_service.py
```

## 数据库设计（SQLite + SQLAlchemy）

### 1. 账户体系 - `investor_account`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| account_no | String(32) UNIQUE | 交易账号（自动生成） |
| name | String(64) | 投资者姓名 |
| id_type | String(16) | 证件类型（身份证/护照/军官证） |
| id_no | String(32) | 证件号码 |
| bank_card_no | String(32) | 银行卡号 |
| phone | String(16) | 手机号 |
| status | String(8) | 账户状态（ACTIVE/FROZEN/CANCELLED） |
| created_at | DateTime | 开户时间 |

### 2. 基金产品 - `fund_product`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| fund_code | String(16) UNIQUE | 基金代码 |
| fund_name | String(64) | 基金名称 |
| nav | Float | 单位净值 |
| nav_date | String(8) | 净值日期（格式：YYYY-MM-DD） |
| status | String(8) | 产品状态（ACTIVE/SUSPENDED） |
| created_at | DateTime | 创建时间 |

> 注：基金产品字段与 Excel 模板列一一对应。交易相关参数（最低申购金额、最低赎回份额、费率等）使用系统默认常量。

### 3. 交易体系 - `trade_order`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| trade_no | String(32) UNIQUE | 交易流水号（自动生成） |
| account_no | String(32) FK | 交易账号 |
| fund_code | String(16) FK | 基金代码 |
| trade_type | String(16) | 交易类型（SUBSCRIBE/REDEEM） |
| amount | Float | 交易金额/份额 |
| nav | Float | 成交净值 |
| fee | Float | 手续费 |
| shares | Float | 确认份额（申购）/ 赎回份额 |
| status | String(16) | 交易状态（PENDING/CONFIRMED/FAILED） |
| trade_time | DateTime | 交易时间 |
| confirm_time | DateTime | 确认时间 |

### 4. 份额体系 - `share_record`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增主键 |
| account_no | String(32) FK | 交易账号 |
| fund_code | String(16) FK | 基金代码 |
| total_shares | Float | 持有总份额 |
| frozen_shares | Float | 冻结份额 |
| available_shares | Float | 可用份额 |
| updated_at | DateTime | 最后更新时间 |

## 基金产品配置（`data/funds.xlsx`）

Excel 文件包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| 基金名称 | 基金产品全称 | 测试基金1 |
| 基金代码 | 唯一基金编码 | 000001 |
| 基金净值 | 单位净值 | 1.1012 |
| 净值日期 | 净值对应日期 | 20260915 |

示例数据：

| 基金名称 | 基金代码 | 基金净值 | 净值日期 |
|----------|----------|----------|----------|
| 测试基金1 | 000001 | 1.1012 | 20260915 |
| 测试基金2 | 000002 | 1.0032 | 20260916 |
| 测试基金3 | 000003 | 3.8923 | 20260917 |
| 测试基金4 | 000004 | 9.8971 | 20260918 |

## API 路由设计

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 首页导航 |
| GET/POST | `/api/v1/accounts/register` | 开户注册 |
| GET | `/api/v1/accounts/<account_no>` | 查询账户信息 |
| GET | `/api/v1/funds` | 查询产品列表（JSON） |
| GET | `/api/v1/funds/list` | 基金产品列表页面 |
| GET/POST | `/api/v1/trades/subscribe` | 申购下单 |
| GET/POST | `/api/v1/trades/redeem` | 赎回下单 |
| GET | `/api/v1/trades/<trade_no>` | 查询交易详情 |
| GET | `/api/v1/shares/<account_no>` | 查询持有份额 |
| GET | `/api/v1/reconciliation/report` | 对账报告 |
| POST | `/api/v1/funds/import` | 从 Excel 导入产品配置 |

## 核心业务逻辑

### 开户注册
1. 校验四要素（姓名、证件类型、证件号、银行卡号）+ 手机号
2. 证件号码唯一性检查（同一证件不可重复开户）
3. 自动生成交易账号（格式：`ACC` + 时间戳 + 随机数）
4. 返回开户结果及交易账号

### 申购交易
1. 校验账户状态、产品状态
2. 校验最低申购金额（默认 1000 元）
3. 计算申购费用 = 申购金额 * 费率（默认 0%）
4. 计算确认份额 = (申购金额 - 手续费) / 净值
5. 生成交易流水号，创建交易记录
6. 确认交易后更新份额记录

### 赎回交易
1. 校验账户状态、产品状态
2. 校验可用份额是否充足
3. 校验最低赎回份额（默认 100 份）
4. 计算赎回金额 = 赎回份额 * 净值
5. 计算赎回费用 = 赎回金额 * 费率（默认 0%）
6. 确认交易后扣减份额

### 对账
1. 汇总所有交易记录（按产品、按交易类型）
2. 核对份额总量 = 所有投资者份额之和
3. 生成对账报告

## 前端页面

- **首页**：系统导航，展示功能入口，含产品导入和查看列表入口
- **基金列表页**：展示所有已导入的基金产品信息
- **开户注册页**：表单输入四要素 + 手机号，提交后展示开户结果
- **申购下单页**：选择账户、选择基金产品、输入申购金额，展示份额计算
- **赎回下单页**：选择账户、选择基金产品、输入赎回份额，展示金额计算
- **份额查询页**：输入交易账号，展示持有各基金份额明细
- **对账报告页**：展示全量对账汇总数据

## 实施步骤

### Step 1: 项目骨架搭建
- 创建目录结构
- 编写 `requirements.txt`（Flask, Flask-SQLAlchemy, openpyxl）
- 编写 `config.py`、`app.py` 入口
- 编写 `.gitignore`
- 初始化 Git 仓库

### Step 2: 数据模型层
- 编写 `models/` 下四个模型文件
- 创建 `data/funds.xlsx` 产品 Excel 配置

### Step 3: 业务服务层
- 编写 `services/fund_loader.py`（Excel 产品导入）
- 编写 `services/account_service.py`（开户/查询）
- 编写 `services/trade_service.py`（申购/赎回）
- 编写 `services/share_service.py`（份额管理）
- 编写 `services/reconciliation_service.py`（对账）

### Step 4: API 路由层
- 编写 `blueprints/` 下四个路由模块
- 注册 Blueprint 到 app
- 添加基金列表页面路由

### Step 5: 前端页面
- 编写 `templates/base.html` 基础布局（Bootstrap 5）
- 编写各业务页面模板（含基金列表页）

### Step 6: 测试与提交
- 编写核心服务单元测试
- 初始化 Git 仓库并提交
- 编写 README.md
