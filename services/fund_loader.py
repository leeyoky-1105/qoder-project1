"""基金产品文件导入服务."""
import json
import logging
from datetime import datetime

from models import db
from models.fund import FundProduct

logger = logging.getLogger(__name__)


class FundLoaderService:
    """基金产品导入服务.

    从 JSON 配置文件加载基金产品信息到数据库.
    """

    @staticmethod
    def import_funds(config_path: str) -> dict:
        """从 JSON 文件导入基金产品.

        Args:
            config_path: JSON 配置文件路径.

        Returns:
            dict: 导入结果，包含成功/失败数量.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error("读取产品配置文件失败: %s", e)
            return {
                "code": 400,
                "message": f"配置文件读取失败: {e}",
                "data": None,
            }

        success_count = 0
        fail_count = 0
        errors = []

        for item in data.get("funds", []):
            try:
                existing = FundProduct.query.filter_by(
                    fund_code=item["fund_code"]
                ).first()

                nav_date = datetime.strptime(
                    item["nav_date"], "%Y-%m-%d"
                ).date()

                if existing:
                    existing.fund_name = item["fund_name"]
                    existing.fund_type = item["fund_type"]
                    existing.nav = item["nav"]
                    existing.nav_date = nav_date
                    existing.min_subscribe = item["min_subscribe"]
                    existing.min_redeem = item["min_redeem"]
                    existing.subscribe_fee_rate = item["subscribe_fee_rate"]
                    existing.redeem_fee_rate = item["redeem_fee_rate"]
                    existing.status = item.get("status", "ACTIVE")
                else:
                    fund = FundProduct(
                        fund_code=item["fund_code"],
                        fund_name=item["fund_name"],
                        fund_type=item["fund_type"],
                        nav=item["nav"],
                        nav_date=nav_date,
                        min_subscribe=item["min_subscribe"],
                        min_redeem=item["min_redeem"],
                        subscribe_fee_rate=item["subscribe_fee_rate"],
                        redeem_fee_rate=item["redeem_fee_rate"],
                        status=item.get("status", "ACTIVE"),
                    )
                    db.session.add(fund)

                success_count += 1
            except Exception as e:
                logger.warning(
                    "导入基金 %s 失败: %s",
                    item.get("fund_code", "unknown"),
                    e,
                )
                fail_count += 1
                errors.append(str(e))

        db.session.commit()
        logger.info(
            "产品导入完成: 成功 %d, 失败 %d",
            success_count,
            fail_count,
        )

        return {
            "code": 0,
            "message": "success",
            "data": {
                "success_count": success_count,
                "fail_count": fail_count,
                "errors": errors,
            },
        }
