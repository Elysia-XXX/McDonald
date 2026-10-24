#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麦门省钱助手 — 本地比价脚本

把麦当劳 MCP `calculate-price` 的多组计算结果整理成 JSON，
本脚本按「应付总价」排序并输出比价表，标出最省组合。

JSON 结构（见 examples/price_combos.sample.json）：
{
  "store": "门店名",
  "combos": [
    {
      "name": "组合名",
      "items": [{"code": "...", "name": "...", "price": 12.0}, ...],
      "delivery_fee": 9.0,        # 堂食可为 0
      "coupon_used": "券描述",     # 可省略
      "discount": 3.5             # 可省略，默认 0
    }
  ]
}

用法：
    python compare_combos.py examples/price_combos.sample.json

说明：商品金额以 calculate-price 返回为准；本脚本只做汇总与排序，
不做任何价格估算，保证比价结论与 MCP 返回一致。
"""

import json
import sys


def load(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "combos" not in data or not data["combos"]:
        raise ValueError("JSON 中缺少非空的 combos 字段")
    return data


def settle(combo: dict) -> dict:
    """汇总一组 calculate-price 结果，计算应付总价。"""
    goods = round(sum(float(i["price"]) for i in combo.get("items", [])), 2)
    delivery = round(float(combo.get("delivery_fee", 0) or 0), 2)
    discount = round(float(combo.get("discount", 0) or 0), 2)
    payable = round(goods + delivery - discount, 2)
    return {
        "name": combo.get("name", "未命名组合"),
        "goods": goods,
        "delivery": delivery,
        "discount": discount,
        "coupon": combo.get("coupon_used", "-"),
        "payable": payable,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    data = load(sys.argv[1])
    rows = sorted((settle(c) for c in data["combos"]), key=lambda r: r["payable"])
    best = rows[0]

    print(f"\n门店：{data.get('store', '-')}")
    print(f"{'组合':<28}{'商品':>8}{'配送费':>8}{'优惠':>8}{'应付':>9}  券")
    print("-" * 76)
    for r in rows:
        tag = "  ★最省" if r is best else ""
        print(
            f"{r['name']:<28}{r['goods']:>8.2f}{r['delivery']:>8.2f}"
            f"{r['discount']:>8.2f}{r['payable']:>9.2f}  {r['coupon']}{tag}"
        )
    print("-" * 76)
    if len(rows) > 1:
        saving = round(rows[1]["payable"] - best["payable"], 2)
        print(f"推荐：{best['name']}，比次优方案省 ¥{saving:.2f}\n")
    else:
        print(f"仅一组候选：应付 ¥{best['payable']:.2f}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
