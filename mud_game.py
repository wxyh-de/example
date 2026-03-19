class Player:
    """玩家类，用于存储角色状态"""
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.hp = 100
        self.exp = 0

    def fight(self):
        """模拟战斗：增加经验，减少血量"""
        self.exp += 10
        self.hp = max(0, self.hp - 20)

    def get_status(self):
        """返回当前角色状态字符串"""
        return f"角色：{self.name} | 等级：{self.level} | 血量：{self.hp} | 经验：{self.exp}"

def main():
    """主游戏循环"""
    player = None
    print("=== 欢迎来到文字 MUD 游戏 ===")
    print("可用命令：create <名字>, fight, status, quit")

    while True:
        command = input("\n请输入命令：").strip().split()
        if not command:
            continue
        
        action = command[0]

        if action == "create":
            if len(command) < 2:
                print("❌ 用法：create 角色名")
                continue
            if player:
                print("❌ 角色已存在，无法重复创建。")
            else:
                player = Player(command[1])
                print(f"✅ 角色 {player.name} 创建成功！")

        elif action == "fight":
            if not player:
                print("❌ 请先创建角色 (create 角色名)。")
            else:
                player.fight()
                print("⚔️ 战斗结束！获得 10 经验，损失 20 血量。")
                if player.hp == 0:
                    print("⚠️ 警告：你的血量已耗尽！")

        elif action == "status":
            if not player:
                print("❌ 请先创建角色。")
            else:
                print("📊 " + player.get_status())

        elif action == "quit":
            print("👋 游戏退出。")
            break
        
        else:
            print("❌ 未知命令，请重试。")

if __name__ == "__main__":
    main()
