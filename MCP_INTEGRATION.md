# MCP_INTEGRATION.md — 麦当劳 MCP 接入说明

## 接入的 MCP Server

| 项 | 值 |
|---|---|
| Server 名称 | 麦当劳中国 MCP Server（mcd-mcp） |
| 接入地址 | `https://mcp.mcd.cn` |
| 传输协议 | Streamable HTTP |
| 鉴权方式 | 请求头 `Authorization: Bearer <MCP Token>` |
| Token 申请 | https://open.mcd.cn/mcp （登录 → 控制台 → 激活） |
| 限流 | 600 次/分钟，超限返回 429 |

## WorkBuddy 接入配置

在 WorkBuddy【连接器 → 自定义连接器 → 配置 MCP】中填入：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      }
    }
  }
}
```

> `YOUR_MCP_TOKEN` 需替换为实际 Token。Token 属敏感信息，请勿提交到任何公开仓库。

## 本项目实际使用的 Tool 清单

### 工作流一：一键薅券

| Tool | 用途 |
|---|---|
| `now-time-info` | 获取当前时间，作为券有效期判断基准 |
| `available-coupons` | 查询麦麦省当前可领取的优惠券列表 |
| `auto-bind-coupons` | 一键领取全部可用优惠券 |
| `query-my-coupons` | 查询用户已有优惠券，回查领券结果 |

### 工作流二：省钱点餐（核心）

| Tool | 用途 |
|---|---|
| `delivery-query-addresses` | 外送：查用户可配送地址 |
| `delivery-create-address` | 外送：新增配送地址 |
| `delivery-query-stores` | 外送：查地址附近可配送门店 |
| `query-nearby-stores` | 到店：查附近可用门店 |
| `query-meals` | 查当前门店可售菜单 |
| `query-meal-detail` | 查套餐构成与可替换选项 |
| `query-store-coupons` | 查当前门店可用优惠券 |
| `calculate-price` | 按商品列表（可含券）计算金额、配送费、优惠与应付总价 |
| `create-order` | 创建订单，返回支付链接（需用户确认） |
| `cancel-order` | 取消订单（需用户确认） |
| `query-order` / `order-list` | 订单详情 / 历史订单 |

### 工作流三：预算 / 热量搭配

| Tool | 用途 |
|---|---|
| `list-nutrition-foods` | 餐品营养数据（能量、蛋白质、脂肪、碳水、钠等） |
| `query-meals` + `calculate-price` | 在预算/热量约束下组合并验证真实价格 |

### 工作流四：积分管家

| Tool | 用途 |
|---|---|
| `query-my-account` | 积分账户：可用/累计/即将过期积分 |
| `mall-points-products` | 麦麦商城可兑换商品列表 |
| `mall-product-detail` | 商品详情 |
| `mall-create-order` | 积分兑换下单，返回券码（需用户确认） |
| `mall-order-list` / `mall-order-detail` | 商城订单查询 |

### 补充能力

| Tool | 用途 |
|---|---|
| `query-lottery-info` / `draw-lottery` / `query-my-prizes` | 积分抽奖（消耗积分，需用户确认） |
| `query-party-city` → `query-party-store` → `query-partystore-date` → `query-partystore-session` → `party-order-create` | 主题活动（派对/品鉴会）查询与预约 |

## 调用流程

### 省钱点餐主流程

```
用户需求（吃什么/预算）
        │
        ▼
[场景判断] ──外送──▶ delivery-query-addresses ─▶ delivery-query-stores
        │                                              │
        └────到店──▶ query-nearby-stores ──────────────┤
                                                       ▼
                                                 query-meals（菜单）
                                                       │
                                                       ▼
                                              query-meal-detail（套餐构成）
                                                       │
                                                       ▼
                                    query-store-coupons + query-my-coupons（查券）
                                                       │
                                                       ▼
                                calculate-price × N（每组候选代入可用券）
                                                       │
                                                       ▼
                                        比价表 → 推荐最省组合 → 用户确认
                                                       │
                                                       ▼
                                                  create-order
                                                       │
                                                       ▼
                                      返回订单号 + 支付链接（query-order 跟踪）
```

### 一键薅券流程

```
now-time-info ─▶ available-coupons ─▶ 展示券列表 ─▶ 用户确认 ─▶ auto-bind-coupons ─▶ query-my-coupons（回查）
```

## 业务价值

1. **真实比价**：普通点餐 App 只展示单品价，优惠券与配送费要自己心算。本 Skill 用 `calculate-price` 拿含券、含配送费的真实应付价做多组合对比，推荐结论可验证。
2. **降低薅券门槛**：麦麦省的券分散在不同入口，`auto-bind-coupons` 一次领完，`query-my-coupons` 统一管理。
3. **营养 + 预算双约束**：`list-nutrition-foods` 让"按热量吃麦当劳"成为一句话的事。
4. **积分不浪费**：主动监控即将过期积分并推荐兑换，减少沉没成本。
5. **安全可控**：所有花钱操作（下单、抽奖、兑换）强制二次确认，杜绝误扣费。
