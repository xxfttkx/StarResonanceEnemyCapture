from logging_config import get_logger


logger = get_logger(__name__)

class EnemyManager:
    """网络数据包抓取器"""
    def __init__(self):
        self.logger = logger
        self.enemies = {}
    
    def sync_enemy(self, id, name, hp, max_hp):
        """同步敌人数据"""
        if not id:
            return
        enemy = self.enemies.get(id, {})
        if name:
            enemy['name'] = name
        if hp:
            enemy['hp'] = hp
        if max_hp:
            enemy['max_hp'] = max_hp
        self.enemies[id] = enemy
        self.logger.info(f"同步敌人数据: {id} -> {enemy['name']}, HP: {enemy['hp']}/{enemy['max_hp']}")