import unittest
from mud_game import Player

class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        """测试玩家初始化功能"""
        player = Player("TestPlayer")
        self.assertEqual(player.name, "TestPlayer")
        self.assertEqual(player.level, 1)
        self.assertEqual(player.hp, 100)
        self.assertEqual(player.exp, 0)
    
    def test_fight_method(self):
        """测试战斗方法"""
        player = Player("TestPlayer")
        initial_exp = player.exp
        initial_hp = player.hp
        
        player.fight()
        
        self.assertEqual(player.exp, initial_exp + 10)
        self.assertEqual(player.hp, initial_hp - 20)
    
    def test_get_status_method(self):
        """测试获取状态方法"""
        player = Player("TestPlayer")
        status = player.get_status()
        self.assertIn("角色：TestPlayer", status)
        self.assertIn("等级：1", status)
        self.assertIn("血量：100", status)
        self.assertIn("经验：0", status)

if __name__ == "__main__":
    unittest.main()
