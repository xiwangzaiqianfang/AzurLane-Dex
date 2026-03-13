import json
import os
from models import Ship

class ShipManager:
    REQUIRED_FIELDS = set(Ship.__dataclass_fields__.keys())

    def __init__(self, filepath="ships.json"):
        self.filepath = filepath
        self.ships: list[Ship] = []
        self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            self._create_sample_data()
            return

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            ship_fields = self.REQUIRED_FIELDS
            migrated = []

            for item in data:
                # 旧数据迁移：如果存在旧式单字段科技点，将其转换为三阶段字段
                self._migrate_old_tech_fields(item)

                # 补全所有缺失字段
                for field in ship_fields:
                    if field not in item:
                        default_val = Ship.__dataclass_fields__[field].default
                        item[field] = default_val

                # 处理 drop_locations
                if isinstance(item.get('drop_locations'), str):
                    item['drop_locations'] = item['drop_locations'].split(';') if item['drop_locations'] else []

                # 仅保留合法字段
                filtered_item = {k: v for k, v in item.items() if k in ship_fields}
                migrated.append(filtered_item)

            self.ships = [Ship.from_dict(item) for item in migrated]

        except json.JSONDecodeError as e:
            raise Exception(f"JSON 文件损坏: {e}\n请使用在线校验工具修复或恢复备份。")

    def _migrate_old_tech_fields(self, item: dict):
        """
        将旧版本的单字段科技点（如 tech_durability）转换为三阶段字段
        （获得阶段赋原值，满破和120阶段置0）
        """
        tech_bases = [
            "tech_durability", "tech_firepower", "tech_torpedo", "tech_aa",
            "tech_aviation", "tech_accuracy", "tech_reload", "tech_mobility", "tech_antisub"
        ]
        for base in tech_bases:
            old_key = base
            if old_key in item and isinstance(item[old_key], (int, float)):
                # 将原值赋给获得阶段
                item[f"{base}_obtain"] = int(item[old_key])
                # 如果满破/120阶段不存在，则设为0
                if f"{base}_max" not in item:
                    item[f"{base}_max"] = 0
                if f"{base}_120" not in item:
                    item[f"{base}_120"] = 0
                # 删除旧字段
                del item[old_key]

    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([s.to_dict() for s in self.ships], f, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {self.filepath}")

    def _create_sample_data(self):
        sample = [
            Ship(
                id=1, name="泛用型布里", faction="其他", ship_class="驱逐", rarity="精锐",
                owned=False, breakthrough=0, oath=False, level_120=False, acquire_main="兑换、赠送", acquire_detail="日/周常任务、月度签到、活动任务、商店兑换、主线普通关卡三星奖励、新兵训练、礼包购买", shop_exchange="勋章、演习", release_date="2017年05月25日", notes="无法建造",
                tech_durability_obtain=0, tech_durability_max=0, tech_durability_120=0,
                tech_firepower_obtain=0, tech_firepower_max=0, tech_firepower_120=0,
                tech_torpedo_obtain=0, tech_torpedo_max=0, tech_torpedo_120=0,
                tech_aa_obtain=0, tech_aa_max=0, tech_aa_120=0,
                tech_aviation_obtain=0, tech_aviation_max=0, tech_aviation_120=0,
                tech_accuracy_obtain=0, tech_accuracy_max=0, tech_accuracy_120=0,
                tech_reload_obtain=0, tech_reload_max=0, tech_reload_120=0,
                tech_mobility_obtain=0, tech_mobility_max=0, tech_mobility_120=0,
                tech_antisub_obtain=0, tech_antisub_max=0, tech_antisub_120=0,
                image_path="images/bulin.png"
            ),
            Ship(
                id=2, name="试作型布里MKII", faction="其他", ship_class="驱逐", rarity="超稀有",
                owned=False, breakthrough=0, oath=False, level_120=False, acquire_main="兑换、赠送", acquire_detail="日/周常任务、月度签到、活动任务、商店兑换、主线普通关卡三星奖励、新兵训练、礼包购买", shop_exchange="勋章、演习", release_date="2017年05月25日", notes="无法建造",
                tech_durability_obtain=0, tech_durability_max=0, tech_durability_120=0,
                tech_firepower_obtain=0, tech_firepower_max=0, tech_firepower_120=0,
                tech_torpedo_obtain=0, tech_torpedo_max=0, tech_torpedo_120=0,
                tech_aa_obtain=0, tech_aa_max=0, tech_aa_120=0,
                tech_aviation_obtain=0, tech_aviation_max=0, tech_aviation_120=0,
                tech_accuracy_obtain=0, tech_accuracy_max=0, tech_accuracy_120=0,
                tech_reload_obtain=0, tech_reload_max=0, tech_reload_120=0,
                tech_mobility_obtain=0, tech_mobility_max=0, tech_mobility_120=0,
                tech_antisub_obtain=0, tech_antisub_max=0, tech_antisub_120=0,
                image_path="images/trial_bulin_mkii.png"
            )
        ]
        self.ships = sample
        self.save()

    def filter(self, criteria: dict) -> list[Ship]:
        result = self.ships[:]
        for field, value in criteria.items():
            if value is None or value == "":
                continue
            if field == "faction":
                result = [s for s in result if s.faction == value]
            elif field == "ship_class":
                result = [s for s in result if s.ship_class == value]
            elif field == "rarity":
                result = [s for s in result if s.rarity == value]
            elif field == "can_remodel" and value:
                result = [s for s in result if s.can_remodel]
            elif field == "remodeled" and value:
                result = [s for s in result if s.remodeled]
            elif field == "oath" and value:
                result = [s for s in result if s.oath]
            elif field == "owned" and value:
                result = [s for s in result if s.owned]
            elif field == "max_breakthrough" and value:
                result = [s for s in result if s.is_max_breakthrough()]
            elif field == "level_120" and value:
                result = [s for s in result if s.level_120]
        return result

    def sort(self, ships: list[Ship], key: str, reverse: bool = False) -> list[Ship]:
        if key == "id":
            return sorted(ships, key=lambda s: s.id, reverse=reverse)
        elif key == "name":
            return sorted(ships, key=lambda s: s.name, reverse=reverse)
        elif key == "rarity":
            rarity_order = {"普通":1, "稀有":2, "精锐":3, "超稀有":4, "海上传奇":5}
            return sorted(ships, key=lambda s: rarity_order.get(s.rarity, 0), reverse=reverse)
        return ships

    def stats(self):
        not_owned = [s for s in self.ships if not s.owned]
        owned_not_max = [s for s in self.ships if s.owned and not s.is_max_breakthrough()]
        return len(not_owned), len(owned_not_max)

    def add_ship(self, ship: Ship):
        max_id = max((s.id for s in self.ships), default=0)
        ship.id = max_id + 1
        self.ships.append(ship)
        self.save()
        print(f"已添加舰船 ID={ship.id}, 当前总数为 {len(self.ships)}")
        return ship.id

    def switch_file(self, new_path):
        self.filepath = new_path
        self.load()

    def export_csv(self, path):
        import pandas as pd
        df = pd.DataFrame([s.to_dict() for s in self.ships])
        df.to_csv(path, index=False, encoding='utf-8-sig')

    def export_excel(self, path):
        import pandas as pd
        df = pd.DataFrame([s.to_dict() for s in self.ships])
        df.to_excel(path, index=False)

    def import_csv(self, path):
        import pandas as pd
        df = pd.read_csv(path, encoding='utf-8-sig')
        ships = []
        for _, row in df.iterrows():
            data = row.to_dict()
            for field in self.REQUIRED_FIELDS:
                if field not in data:
                    data[field] = Ship.__dataclass_fields__[field].default
            ships.append(Ship.from_dict(data))
        self.ships = ships
        self.save()

    def update_from_github(self, url):
        import requests
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
            # 数据迁移和验证（类似 load 中的处理）
            # ...
            self.ships = [Ship.from_dict(item) for item in data]
            self.save()
        except Exception as e:
            raise Exception(f"网络更新失败: {e}")