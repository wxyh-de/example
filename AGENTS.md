# MUD 游戏项目 AGENTS 文档

## 项目架构概述
- **项目类型**：文字 MUD 游戏
- **技术栈**：Python 3.7+
- **核心模块**：Player 类（角色管理）、主游戏循环（命令处理）
- **测试框架**：Python unittest

## 目录结构说明
```
├── mud_game.py        # 核心游戏逻辑
├── test_mud_game.py   # 单元测试
├── README.md          # 项目文档
├── AGENTS.md          # 本文件
└── .github/workflows/
    └── ci.yml         # CI 配置
```

## 核心模块职责

### Player 类
- **职责**：管理玩家角色状态和行为
- **核心方法**：
  - `__init__(name)`：初始化角色
  - `fight()`：模拟战斗
  - `add_item(item_name, quantity)`：添加物品
  - `remove_item(item_name, quantity)`：移除物品
  - `trade_item(other_player, item_name, quantity)`：交易物品
  - `get_status()`：获取角色状态
  - `get_inventory()`：获取背包内容

### 主游戏循环
- **职责**：处理用户输入命令，协调游戏流程
- **支持命令**：create, fight, status, quit, add, inventory, create_other, trade

## 编码规范约束
- **命名规范**：使用小写蛇形命名法（snake_case）
- **缩进**：4 空格缩进
- **注释**：为所有类和方法添加文档字符串
- **异常处理**：对用户输入进行合理的错误处理
- **测试**：为核心功能编写单元测试

## 禁止操作清单
- 禁止修改核心游戏逻辑的基础结构
- 禁止添加外部依赖
- 禁止使用未经过测试的代码
- 禁止在主游戏循环中添加复杂的业务逻辑
- 禁止修改 CI 配置文件的基本结构