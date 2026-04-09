# 详细设计说明书 (DDS) 更新

## 核心控制类分析

### 1. GameEngine 类

#### 1.1 process\_command 方法 N-S盒图

```
[开始]
    |
    v
[command_parts = input_str.strip().split()]
    |
    v
[if not command_parts]
    |--- [是] ---> [return ""]
    |
    v [否]
[action = command_parts[0]]
    |
    v
[if action not in self.commands]
    |--- [是] ---> [return "❌ 未知命令，请重试。"]
    |
    v [否]
[if action == "create" and len(command_parts) < 2]
    |--- [是] ---> [return "❌ 用法：create 角色名"]
    |
    v [否]
[if action == "create"]
    |--- [是] ---> [command = self.commands[action](command_parts[1])]
    |
    v [否]
[command = self.commands[action]()]
    |
    v
[return command.execute(self)]
    |
    v
[结束]
```

#### 1.2 run 方法 N-S盒图

```
[开始]
    |
    v
[print("=== 欢迎来到文字 MUD 游戏 ===")]
    |
    v
[print("可用命令：create <名字>, fight, status, quit")]
    |
    v
[while self.running]
    |   |
    |   v
    |[command = input("\n请输入命令：")]
    |   |
    |   v
    |[result = self.process_command(command)]
    |   |
    |   v
    |[if result]
    |   |--- [是] ---> [print(result)]
    |   |
    |   v [否]
    |[继续循环]
    |
    v
[结束]
```

### 2. Player 类

#### 2.1 fight 方法 N-S盒图

```
[开始]
    |
    v
[self.exp += 10]
    |
    v
[self.hp = max(0, self.hp - 20)]
    |
    v
[return self.hp]
    |
    v
[结束]
```

#### 2.2 level\_up 方法 N-S盒图

```
[开始]
    |
    v
[if self.exp >= 100]
    |--- [是] ---> [self.level += 1]
    |               |
    |               v
    |           [self.exp -= 100]
    |               |
    |               v
    |           [self.hp = 100]
    |               |
    |               v
    |           [return True]
    |
    v [否]
[return False]
    |
    v
[结束]
```

### 3. Command 子类

#### 3.1 CreateCommand.execute 方法 N-S盒图

```
[开始]
    |
    v
[if game_engine.player]
    |--- [是] ---> [return "❌ 角色已存在，无法重复创建。"]
    |
    v [否]
[game_engine.player = Player(self.name)]
    |
    v
[return f"✅ 角色 {self.name} 创建成功！"]
    |
    v
[结束]
```

#### 3.2 FightCommand.execute 方法 N-S盒图

```
[开始]
    |
    v
[if not game_engine.player]
    |--- [是] ---> [return "❌ 请先创建角色 (create 角色名)。"]
    |
    v [否]
[hp = game_engine.player.fight()]
    |
    v
[message = "⚔️ 战斗结束！获得 10 经验，损失 20 血量。"]
    |
    v
[if hp == 0]
    |--- [是] ---> [message += "\n⚠️ 警告：你的血量已耗尽！"]
    |
    v [否]
[if game_engine.player.level_up()]
    |--- [是] ---> [message += f"\n🎉 恭喜 {game_engine.player.name} 升级到 {game_engine.player.level} 级！"]
    |
    v [否]
[return message]
    |
    v
[结束]
```

## 跨类调用方法签名

### 1. GameEngine 类方法签名

| 方法名               | 参数              | 返回值 | 说明        |
| ----------------- | --------------- | --- | --------- |
| `__init__`        | 无               | 无   | 初始化游戏引擎   |
| `process_command` | input\_str: str | str | 处理用户输入的命令 |
| `run`             | 无               | 无   | 运行游戏主循环   |

### 2. Player 类方法签名

| 方法名          | 参数        | 返回值  | 说明              |
| ------------ | --------- | ---- | --------------- |
| `__init__`   | name: str | 无    | 初始化玩家对象         |
| `fight`      | 无         | int  | 执行战斗逻辑，返回当前血量   |
| `get_status` | 无         | str  | 返回玩家状态字符串       |
| `level_up`   | 无         | bool | 执行升级逻辑，返回是否升级成功 |

### 3. Command 类方法签名

| 方法名       | 参数                       | 返回值 | 说明            |
| --------- | ------------------------ | --- | ------------- |
| `execute` | game\_engine: GameEngine | str | 执行命令逻辑，返回结果信息 |

### 4. CreateCommand 类方法签名

| 方法名        | 参数                       | 返回值 | 说明        |
| ---------- | ------------------------ | --- | --------- |
| `__init__` | name: str                | 无   | 初始化创建角色命令 |
| `execute`  | game\_engine: GameEngine | str | 执行创建角色逻辑  |

### 5. FightCommand 类方法签名

| 方法名        | 参数                       | 返回值 | 说明      |
| ---------- | ------------------------ | --- | ------- |
| `__init__` | 无                        | 无   | 初始化战斗命令 |
| `execute`  | game\_engine: GameEngine | str | 执行战斗逻辑  |

### 6. StatusCommand 类方法签名

| 方法名        | 参数                       | 返回值 | 说明        |
| ---------- | ------------------------ | --- | --------- |
| `__init__` | 无                        | 无   | 初始化查看状态命令 |
| `execute`  | game\_engine: GameEngine | str | 执行查看状态逻辑  |

### 7. QuitCommand 类方法签名

| 方法名        | 参数                       | 返回值 | 说明        |
| ---------- | ------------------------ | --- | --------- |
| `__init__` | 无                        | 无   | 初始化退出游戏命令 |
| `execute`  | game\_engine: GameEngine | str | 执行退出游戏逻辑  |

