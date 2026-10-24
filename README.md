# 麦门省钱助手（mcd-saver）

> 基于麦当劳中国 MCP 能力开发的 AI 点餐省钱 Skill —— 用最少的钱，吃到想吃的麦麦。

## 项目介绍

「麦门省钱助手」是一个面向 WorkBuddy 的 Skill（技能包），基于麦当劳中国官方 MCP Server（`https://mcp.mcd.cn`）编排了四条省钱工作流：

| 工作流 | 场景 | 用到的核心 MCP 能力 |
|---|---|---|
| 一键薅券 | 把当前可领的券一次领光 | 麦麦省券列表、一键领券、我的券查询 |
| 省钱点餐 | 选店 → 选品 → 多组合比价 → 下单 | 门店/菜单/券查询、商品价格计算、创建订单 |
| 预算/热量搭配 | "30 块能吃什么" / "600 卡以内配一餐" | 餐品营养数据、菜单、价格计算 |
| 积分管家 | 积分过期提醒、积分兑换不浪费 | 积分账户、麦麦商城商品与兑换 |

核心创意点：**点餐前先比价**。Skill 会强制对候选组合分别调用 `calculate-price`（代入可用优惠券），用真实应付金额（含配送费、优惠金额）做对比，而不是凭感觉推荐。

## 目标用户

- 经常点麦当劳、想省钱但懒得逐个试券的打工人
- 健身/控卡人群，需要按热量目标搭套餐
- 积分多且容易过期的麦麦会员

## 安装方法

### 1. 申请麦当劳 MCP Token

1. 访问麦当劳 MCP 开放平台：https://open.mcd.cn/mcp
2. 手机号登录 → 右上角【控制台】→ 点击【激活】申请 MCP Token
3. 阅读并同意服务协议，复制生成的 Token

### 2. 在 WorkBuddy 中配置 MCP 连接器

WorkBuddy 左侧边栏【专家·技能·连接器】→【连接器】→ 右上角【自定义连接器】→【配置 MCP】，粘贴以下 JSON（替换 `YOUR_MCP_TOKEN`）：

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

保存后回到【自定义连接器】，将 `mcd-mcp` 启用。

### 3. 安装本 Skill

将 `skill/mcd-saver/` 目录复制到 WorkBuddy 用户级技能目录 `~/.workbuddy/skills/`（即 `C:\Users\<你>\.workbuddy\skills\mcd-saver`），重启会话即可生效。

### 4. 开聊

在对话框里试试：

- "帮我把麦当劳的券都领了"
- "我想吃辣的，30 块以内，帮我看看怎么点最划算"
- "帮我配一个 600 卡以内的麦当劳套餐"
- "我的积分快过期了，能换点什么？"

## 使用示例

完整的示例对话剧本见 [examples/demo.md](examples/demo.md)，覆盖领券、比价点餐、预算搭配三个场景。

比价脚本 `scripts/compare_combos.py` 可独立使用：把多组 `calculate-price` 的返回结果整理成 JSON，脚本输出排序后的比价表：

```bash
python scripts/compare_combos.py examples/price_combos.sample.json
```

## 仓库结构

```
mcd-saver-skill/
├── README.md              # 本文件
├── CONTEST_DECLARATION.md # 参赛声明（官方原文，未做任何修改）
├── MCP_INTEGRATION.md     # 麦当劳 MCP 接入说明
├── workbuddy.md           # WorkBuddy 开发对话记录说明
├── skill/mcd-saver/SKILL.md   # Skill 主体
├── examples/              # 示例对话与比价样例数据
└── scripts/               # 本地比价辅助脚本
```

## 声明

- 本项目为 2026 麦当劳程序员创意开发大赛参赛作品，基于麦当劳中国开放的 MCP 能力开发，非麦当劳官方产品。
- 使用本项目需自行申请 MCP Token 并遵守麦当劳中国的《使用条款》及《麦当劳 MCP 服务规则》。
- 涉及真实付款的操作均需用户在对话中二次确认。

## 参赛信息

- 赛事：[M-China/mcd-developer-innovation-challenge](https://github.com/M-China/mcd-developer-innovation-challenge)
- MCP 文档：[M-China/mcd-mcp-server](https://github.com/M-China/mcd-mcp-server)
